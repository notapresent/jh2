# -*- coding: utf-8 -*-
import datetime

from rq import Queue

from .models import Record, Scan, ScanRecord, Image
from . import scraper

JOB_TIMEOUT = 300


class Scheduler(object):
    def __init__(self, session, redis, queue_name):
        self.session = session
        self.redis = redis
        self.queue_name = queue_name
        self.queue = Queue(self.queue_name, connection=self.redis)

    def run_scan(self, genre_id):
        current_scan = Scan.get_current(genre_id, self.session)
        if current_scan:
            raise AlreadyStarted('Scan for genre #{} is already started: '
                                 '{}'.format(genre_id, current_scan))

        self.queue.enqueue('rbm2m.worker.start_scan', genre_id)

    def start_scan(self, genre_id):
        scan = Scan(genre_id=genre_id,
                    started_at=datetime.datetime.utcnow(),
                    status='started')
        self.session.add(scan)
        self.session.commit()
        print "*** Starting scan #{} for genre {}".format(scan.id, genre_id)

        self.queue.enqueue('rbm2m.worker.task', scan.id, timeout=JOB_TIMEOUT)

    def abort_scan(self, scan_id):
        self.finish_scan(scan_id, 'aborted')

    def finish_scan(self, scan_id, status):
        print "*** Scan #{} finished with status {}".format(scan_id, status)
        scan = self.session.query(Scan).get(scan_id)
        scan.status = status
        scan.finished_at = datetime.datetime.utcnow()
        self.session.add(scan)  # TODO really needed?
        self.session.commit()

    def run_task(self, scan_id, page=0):
        # TODO split this method
        scan = self.session.query(Scan).get(scan_id)
        if scan.status == 'aborted':
            return

        try:
            records, next_page, rec_count = scraper.scrape_page(
                scan.genre.title, page)
        except scraper.ScrapeError as e:
            print "*** Scan #{} failed: {}".format(scan_id, e)
            self.queue.enqueue('rbm2m.worker.finish_scan', scan_id, 'failed')
            return

        # Update estimated records count every 10 pages
        if page % 10 == 0:
            self.session.query(Scan).filter_by(id=scan_id) \
                .update({Scan.num_records: rec_count})

        # records: [(id, {values}), ...]
        record_ids = [rid for rid, rec in records]
        existing_records = (
            self.session.query(Record.id)
            .filter(Record.id.in_(record_ids))
            .all()
        )
        existing_ids = [rec_id for (rec_id,) in existing_records]

        fetch_images = []
        for rec_id, rec in records:
            if rec_id in existing_ids:
                continue

            has_images = rec.pop('has_images')
            if has_images:
                fetch_images.append(rec_id)

            record = Record(**rec)
            record.id = rec_id
            record.import_date = datetime.datetime.utcnow()
            record.genre_id = scan.genre_id
            self.session.add(record)

        self.session.flush()

        for rec_id in record_ids:
            self.session.add(ScanRecord(scan_id=scan_id, record_id=rec_id))

        self.session.commit()

        for rec_id in fetch_images:
            self.queue.enqueue('rbm2m.worker.get_images', rec_id,
                               timeout=300,
                               at_front=True)

        print "Scan #{} / page #{} - {} items, {} new".format(
            scan_id, page, len(records), len(records) - len(existing_ids))

        if next_page:
            self.queue.enqueue('rbm2m.worker.task', scan_id, next_page,
                               timeout=JOB_TIMEOUT)
        else:
            self.queue.enqueue('rbm2m.worker.finish_scan', scan_id, 'success')

    def get_images(self, rec_id):
        urls = scraper.image_list(rec_id)

        for img_url in urls:
            self.session.add(Image(record_id=rec_id, source_url=img_url))

        self.session.commit()
        print "Added {} images for record #{}".format(len(urls), rec_id)


class SchedulerError(Exception):
    pass


class AlreadyStarted(SchedulerError):
    pass
