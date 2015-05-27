# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref

from .base import Base


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, autoincrement=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    import_date = Column(DateTime, nullable=False)
    artist = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    label = Column(String(250), nullable=False)
    notes = Column(String(500))
    grade = Column(String(16), nullable=False)
    format = Column(String(2), nullable=False)
    price = Column(Integer)

    genre = relationship("Genre", backref=backref('records', order_by=id))


class RecordStatus(Base):
    __tablename__ = 'record_status'
    record_id = Column(Integer, ForeignKey('records.id'),
                       primary_key=True,
                       autoincrement=False)
    status = Column(String(50), nullable=False)
