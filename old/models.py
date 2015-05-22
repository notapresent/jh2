from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey,
    SmallInteger)
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    search_term = Column(String(50), nullable=False)

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
    price = Column(Integer)     # TODO Numeric?
    img_url = Column(String(250))

    genre = relationship("Genre", backref=backref('records', order_by=id))
#  - status (default, sold)


class Scan(Base):
    __tablename__ = 'scans'
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    num_records = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    records_added = Column(Integer, nullable=False, default=0)
    records_removed = Column(Integer, nullable=False, default=0)
    status = Column(String(50))

    genre = relationship("Genre", backref=backref('scans', order_by=id))
