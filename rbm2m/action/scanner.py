# -*- coding: utf-8 -*-
import datetime
import logging

import task_queue
import scan_manager
import record_importer
import image_importer


logger = logging.getLogger(__name__)


class ScanError(Exception):

    """
        Base exception for this module
    """
    pass


class Scanner(object):

    """
        Controls scan execution process
    """

    def __init__(self, config, session, redis):
        self.config = config
        self.session = session
        self.redis = redis
        self._scan_manager = None
        self._queue = None

    @property
    def scan_manager(self):
        if self._scan_manager is None:
            self._scan_manager = scan_manager.ScanManager(self.session)

        return self._scan_manager

    @property
    def queue(self):
        if self._queue is None:
            self._queue = task_queue.TaskQueue(self.redis)

        return self._queue

    def enqueue_scan(self, genre_id):
        """
            Enqueue new scan for specified genre
        """
        if self.scan_manager.get_current_for_genre(genre_id):
            raise ScanError('Scan already queued')

        scan_dict = {'genre_id': genre_id, 'status': 'queued'}
        scan = self.scan_manager.from_dict(scan_dict)
        self.session.commit()
        self.queue.enqueue('start_scan', scan.id)

    def abort_scan(self, scan_id):
        """
            Aborts scan currently in progress
        """
        scan = self.scan_manager.get(scan_id)

        if not scan:
            raise ScanError('Scan #{} not found'.format(scan_id))

        if scan.status not in ['queued', 'running']:
            raise ScanError('Invalid scan status: {}'.format(scan.status))

        self.finish_scan(scan.id, 'aborted')

    def start_scan(self, scan_id):
        """
            Change scan status to 'running' and enqueue first page task
        """
        scan = self.scan_manager.get(scan_id)
        scan.status = 'running'
        self.queue.enqueue('page_task', scan.id)

    def finish_scan(self, scan_id, status):
        """
            Set scan status and finish date
        """
        logger.info("Scan #{} finished with status {}".format(scan_id, status))
        scan = self.scan_manager.get(scan_id)
        scan.status = status
        scan.finished_at = datetime.datetime.utcnow()

    def page_task(self, scan_id, page_no=None):
        """
            Import records from page and queue next page and/or image import
        """
        scan = self.scan_manager.get(scan_id)
        if scan.status == 'aborted':     # or != 'running'
            return

        imp = record_importer.RecordImporter(self.session, scan)

        try:
            imp.run(scan, page_no)
        except record_importer.RecordImportError as e:
            self.finish_scan(scan.id, 'failed')
            logger.error("Page #{} of scan #{}: {}".format(page_no or 0, scan_id, e))
            return

        if imp.has_images:
            imgjob = self.queue.enqueue('image_task', imp.has_images, at_front=True)
        else:
            imgjob = None

        if imp.next_page:
            self.queue.enqueue('page_task', scan.id, imp.next_page, depends_on=imgjob)
        else:
            self.queue.enqueue('finish_scan', scan.id, 'success', depends_on=imgjob)

        logger.debug("Page #{} of scan #{} completed".format(page_no or 0, scan_id))

    def image_task(self, rec_ids):
        """
            Download and save images for records in rec_ids
        """
        imp = image_importer.ImageImporter(self.config, self.session)
        imp.run(rec_ids)
