# -*- coding: utf-8 -*-
"""
Persistent models, representing rows in DB, along with some helper methods
"""
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean,
                        func)
from sqlalchemy.orm import relationship, backref
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Genre(db.Model):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    import_active = Column(Boolean(), nullable=False, default=False)
    export_active = Column(Boolean(), nullable=False, default=False)


class Record(db.Model):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, autoincrement=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    import_date = Column(DateTime, nullable=False)
    artist = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    label = Column(String(250), nullable=False)
    notes = Column(String(500))
    grade = Column(String(16), nullable=False)
    price = Column(Integer)

    genre = relationship("Genre", backref=backref('records', order_by=id))


class Image(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('records.id'), nullable=False)
    source_url = Column(String(512), nullable=False)


class Scan(db.Model):
    __tablename__ = 'scans'
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    # Estimate based on number of records at the moment of start
    num_pages = Column(Integer)
    status = Column(String(50), nullable=False)

    genre = relationship("Genre", backref=backref('scans', order_by=id))
    # records = relationship("Record")  # TODO many-to-many reltionship

    @classmethod
    def get_last_scans(cls, num=5):
        return cls.query.order_by(-cls.started_at).limit(num).all()


class ScanRecord(db.Model):
    __tablename__ = 'scan_records'
    scan_id = Column(Integer, ForeignKey('scans.id'), primary_key=True)
    record_id = Column(Integer, ForeignKey('records.id'), primary_key=True)


class RecordStatus(db.Model):
    __tablename__ = 'record_status'
    record_id = Column(Integer, ForeignKey('records.id'), primary_key=True,
                       autoincrement=False)
    status = Column(String(50), nullable=False)


def get_stats(session):
    return {
        'records_total': session.query(func.count(Record.id)).scalar(),
        # Number of records in last successful crawl for each genre
        'records_in_stock': 12345,
        'images_total': session.query(func.count(Image.id)).scalar(),
        # Number of records in last succesful crawl for each exported genre
        'lots': 1234,
        # number of failed crawls, at most one for each genre
        'errors': 12
    }
