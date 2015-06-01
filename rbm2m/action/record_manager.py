# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Record


class RecordManager(BaseManager):
    """
        Handles all DB interactions regarding records
    """
    __model__ = Record

    def find_existing(self, rec_ids):
        return (
            self.session.query(self.__model__)
                .filter(self.__model__.id.in_(rec_ids))
                .all()
        )
