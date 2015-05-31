# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Scan
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class ScanManager(BaseManager):
    """
        Handles all DB interactions regarding scans
    """
    __class__ = Scan

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

