# -*- coding: utf-8 -*-
import datetime

from rq import Queue

from .models import Record, Scan, Image
from . import scraper


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

        self.queue.enqueue('rbm2m.worker.task', scan.id)

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
        scan = self.session.query(Scan).get(scan_id)
        if scan.status == 'aborted':
            return
            
        try:
            records, rec_count, next_page = scraper.scrape_page(scan.genre.title, page)
        except scraper.ScrapeError:
            self.queue.enqueue('rbm2m.worker.finish_scan', scan_id, 'failed')
            return

        # Update estimated records count every 10 pages
        if page % 10 == 0:
            self.session.query(Scan).filter_by(id=scan_id) \
                .update({Scan.num_records: rec_count})

        # records: [(id, {values}), ...]
        record_ids = [rid for rid, rec in records]
        existing_ids = self.session.query(Record.id) \
            .filter(Record.id in record_ids) \
            .all()

        for rec_id, rec in records:
            if rec_id in existing_ids:
                continue
            image_urls = rec.pop('images', [])
            record = Record(**rec)
            for img_url in image_urls:
                rec.images.append(Image(url=img_url))
            self.session.add(record)

        self.session.commit()
        print "Scan #{} / page #{} - {} items, {} new".format(
            scan_id, page, len(records), len(records)-len(existing_ids))

        if next_page:
            self.queue.enqueue('rbm2m.worker.task', scan_id, page+1, timeout=300)
        else:
            self.queue.enqueue('rbm2m.worker.finish_scan', scan_id, 'success')


class SchedulerError(Exception):
    pass

class AlreadyStarted(SchedulerError):
    pass
