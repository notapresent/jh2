# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref

from .base import Base


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    # Number of records at the moment of start
    num_records = Column(Integer)
    status = Column(String(50), nullable=False)

    genre = relationship("Genre", backref=backref('scans', order_by=id))
    # records = relationship("Record")  # TODO many-to-many relationship

    @classmethod
    def get_current(cls, genre_id, session):
        return session.query(cls) \
            .filter_by(genre_id=genre_id, status='started') \
            .first()


class ScanRecord(Base):
    __tablename__ = 'scan_records'
    scan_id = Column(Integer, ForeignKey('scans.id'), primary_key=True)
    record_id = Column(Integer, ForeignKey('records.id'), primary_key=True)
