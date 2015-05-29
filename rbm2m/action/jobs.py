# -*- coding: utf-8 -*-


class Job(object):
    session = None
    config = None

    def run(self, *args, **kwargs):
        self._run(*args, **kwargs)

    def _run(self, *args, **kwargs):
        raise NotImplementedError


class StartScanJob(Job):
    def __init__(self, scan):
        self.scan = scan

    def _run(self, *args, **kwargs):
        # call ScanManager.start_scan(self.scan)
        # change scan status to 'running'
        # enqueue 1st task
        pass

class FinishScanJob(Job):
    def __init__(self, scan, status):
        self.scan = scan
        self.status = status

    def _run(self, *args, **kwargs):
        # call ScanManager.finish_scan(self.scan, self.status)
        # change scan status to self.status
        # scan.finished_at = datetime.datetime.utcnow()
        pass


class PageJob(Job):
    def __init__(self, scan_id, page_no=None):
        self.scan_id = scan_id
        self.page_no = page_no

    def _run(self,  *args, **kwargs):
        # call TaskManager.scan
        # if scan aborted - enqueue finish scan
        #
        pass


class ImageJob(Job):
    def __init__(self, record_ids):
        self.record_ids = record_ids

    def _run(self, cfg, sess):
        pass

