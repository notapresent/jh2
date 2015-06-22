# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Scan, scan_records


class ScanManager(BaseManager):

    """
        Handles all DB interactions regarding scans
    """
    __model__ = Scan

    def get_current_for_genre(self, genre_id):
        """
            Returns currently running scans for genre
        """
        return (
            self.session.query(Scan)
            .filter(Scan.genre_id == genre_id)
            .filter(Scan.status.in_(['queued', 'running', 'aborting']))
            .all()
        )

    def last_scans(self):
        return (
            self.session.query(Scan)
            .order_by(Scan.started_at.desc())
            .limit(50)
            .all()
        )

    def records_not_in_scan(self, scan_id, rec_ids):
        result = (self.session.query(scan_records.c.record_id)
            .filter(scan_records.c.scan_id==scan_id)
            .filter(scan_records.c.record_id.in_(rec_ids))
            .all()
        )
        in_scan = [rec_id for rec_id, in result]
        return list(set(rec_ids) - set(in_scan))

