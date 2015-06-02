# -*- coding: utf-8 -*-
from sqlalchemy import or_

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

    def list(self, filters=None, search=None, order='id', offset=0):
        q = self.session.query(Record)

        q = q.filter_by(**filters)

        if search:
            search = '%{}%'.format(search)
            q = q.filter(or_(
                Record.artist.ilike(search),
                Record.title.ilike(search),
                Record.notes.ilike(search),
                Record.label.ilike(search)
            ))

        if order[0] == '-':
            q = q.order_by(getattr(Record, order[1:].desc()))
        else:
            q = q.order_by(getattr(Record, order))

        return q.offset(offset).limit(50).all()
