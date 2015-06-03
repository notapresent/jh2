# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Scan


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
