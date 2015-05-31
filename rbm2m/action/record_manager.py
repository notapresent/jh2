# -*- coding: utf-8 -*-
# record_manager.py
from base_manager import BaseManager
from ..models import Record


class RecordManager(BaseManager):
    """
        Handles all DB interactions regarding records
    """
    def find_existing(self, rec_ids):
        return (
            self.session.query(Record)
                .filter(Record.id.in_(rec_ids))
                .all()
        )
