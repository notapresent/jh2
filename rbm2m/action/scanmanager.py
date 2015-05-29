# -*- coding: utf-8 -*-
from ..models import Scan
from jobs import StartScanJob
from queuemanager import QueueManager

class ScanManager(object):
    """
        Manages scan creation and execution
    """
    def __init__(self, config, session, redis):
        self.config = config
        self.session = session
        self.redis = redis

    def run_scan(self, genre_id):
        """
            Enqueue scan for genre or raise ScanException if there is already
            started or queued scan for this genre
        """
        curr_scan = self.current_scan(genre_id)

        if curr_scan:
            msg = "Scan for #{} already {}".format(genre_id, curr_scan.status)
            raise ScanException(msg)

        scan = Scan(genre_id=genre_id, status='queued')
        self.session.add(scan)
        self.session.flush()
        self.enqueue_scan(scan)

    def abort_scan(self, scan_id):
        """
        Abort queued or started scan or raise TODO
        """
        scan = self.session.query(Scan).get(scan_id)
        if not scan:
            raise ScanException("Invalid scan: {}".format(scan_id))

        scan.status = 'aborting'

    def current_scan(self, genre_id):
        return (self.session.query(Scan)
                .filter(Scan.genre_id == genre_id)
                .filter(Scan.status.in_(['queued', 'running']))
                .first())

    def enqueue_scan(self, scan):
        job = StartScanJob(scan)
        queueman = QueueManager(self.config)
        queueman.enqueue(job)


class ScanException(Exception):
    """
        Base class for all exceptions raised in this module
    """
    pass
