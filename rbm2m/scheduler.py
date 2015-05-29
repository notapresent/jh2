# -*- coding: utf-8 -*-
import datetime

from rq import Queue

from .models import Record, Scan, Image
from . import scraper

JOB_TIMEOUT = 300
RESULT_TIMEOUT = 0


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
            record_dicts, next_page, rec_count = scraper.scrape_page(
                scan.genre.title, page)
        except scraper.ScrapeError as e:
            print "*** Scan #{} failed: {}".format(scan_id, e)
            self.queue.enqueue('rbm2m.worker.finish_scan', scan_id, 'failed')
            return

        # Update estimated records count every 10 pages
        if page % 10 == 0:
            scan.est_num_records = rec_count

        record_ids = [rec['id'] for rec in record_dicts if rec['success']]
        if record_ids:
            existing_records = (
                self.session.query(Record)
                    .filter(Record.id.in_(record_ids))
                    .all()
            )
        else:
            existing_records = []

        for rec in existing_records:
            scan.records.append(rec)

        existing_ids = [rec.id for rec in existing_records]
        fetch_images = []

        for rec in record_dicts:
            if rec['id'] in existing_ids:
                continue

            success = rec.pop('success')
            if not success:
                continue

            has_images = rec.pop('has_images')
            if has_images:
                fetch_images.append(rec['id'])

            record = Record(**rec)
            record.genre_id = scan.genre_id
            scan.records.append(record)

        self.session.commit()

        for rec_id in fetch_images:
            self.queue.enqueue('rbm2m.worker.get_images', rec_id,
                               timeout=JOB_TIMEOUT,
                               at_front=True)

        print "Scan #{} / page #{} - {} items, {} new".format(
            scan_id, page, len(record_dicts), len(record_dicts) - len(existing_ids))

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
