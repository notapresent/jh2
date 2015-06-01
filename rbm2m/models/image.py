# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship, backref

from .base import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey('records.id'), nullable=False)
    record = relationship('Record', backref=backref('images'))

    url = Column(String(512), nullable=False)
    length = Column(Integer)
