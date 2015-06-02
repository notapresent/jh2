# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from sqlalchemy import (Column, Integer, String, Text, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref

from ..helpers import JsonSerializer
from .base import Base

FLAGS = {
    # Marks record that must not appear in export
    'skip': {
        'label': 'Не экспортировать',
        'description': 'Исключить эту запись из экспорта в YML и таблицы',
        'css_class': '',
        'readonly': False

    },
    # Marks record for which one or more images was not imported
    'missing_images': {
        'label': 'Ошибка при загрузке картинок',
        'description': 'Не удалось загрузить одну или несколько картинок для этой записи',
        'css_class': 'alert',
        'readonly': True
    }
}


class Record(Base, JsonSerializer):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, autoincrement=False)
    import_date = Column(DateTime, default=datetime.datetime.utcnow,
                         nullable=False)
    artist = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    label = Column(String(250), nullable=False)
    notes = Column(Text)
    grade = Column(String(16), nullable=False)
    format = Column(String(2), nullable=False)
    price = Column(Integer)

    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    genre = relationship("Genre", uselist=False, lazy='joined',
                         backref=backref('records', lazy='dynamic'))

    flags = relationship('RecordFlag',  lazy='dynamic',
                         backref=backref('record'))


class RecordFlag(Base):
    __tablename__ = 'record_flags'

    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey(Record.id))
    name = Column(String(50), nullable=False)
