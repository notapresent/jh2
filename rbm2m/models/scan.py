# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Table)
from sqlalchemy.orm import relationship, backref

from .base import Base


scan_records = Table(
    'scan_records',
    Base.metadata,
    Column('scan_id', Integer, ForeignKey('scans.id')),
    Column('record_id', Integer, ForeignKey('records.id'))
)


class Scan(Base):
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
    # Estimated number of records
    est_num_records = Column(Integer)
    status = Column(String(50), nullable=False)

    @classmethod
    def get_current(cls, genre_id, session):
        return session.query(cls) \
            .filter_by(genre_id=genre_id, status='started') \
            .first()
