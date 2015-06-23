# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base
from rbm2m.models.base import JsonSerializer

SCAN_STATUSES = {
    'success': 'Успешно завершен',
    'running': 'В процессе',
    'aborted': 'Отменен',
    'queued': 'В очереди',
    'failed': 'Ошибка'
}

scan_records = Table(
    'scan_records',
    Base.metadata,
    Column('scan_id', Integer, ForeignKey('scans.id', ondelete='CASCADE'), primary_key=True),
    Column('record_id', Integer, ForeignKey('records.id', ondelete='CASCADE'), primary_key=True)
)


class Scan(Base, JsonSerializer):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)

    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    genre = relationship("Genre", backref=backref('scans', order_by=id),
                         lazy='joined')

    records = relationship("Record", secondary=scan_records, backref="scans",
                           lazy='dynamic')

    started_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    last_action = Column(DateTime, nullable=True, server_default=func.now(),
                         onupdate=func.current_timestamp())
    # Estimated number of records
    est_num_records = Column(Integer)
    status = Column(String(50), nullable=False)

    @hybrid_property
    def duration(self):
        if self.finished_at:
            return self.finished_at - self.started_at
        else:
            return datetime.datetime.utcnow() - self.started_at
