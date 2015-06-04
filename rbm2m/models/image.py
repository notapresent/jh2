# -*- coding: utf-8 -*-
import os
import urlparse

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

    def make_filename(self, suffix=None):
        """
            Generate filename from id and base dir, with optional suffix
        """
        if suffix is None:
            suffix = normalize_jpg_suffix(url_suffix(self.url))

        strid = str(self.id).zfill(4)
        chunks = [strid[-2:], strid[-4:-2], "{}{}".format(strid, suffix)]
        return os.path.join(*chunks)


def url_suffix(url):
    """
        Extract file extension from url
    """
    path = urlparse.urlparse(url).path
    return os.path.splitext(path)[1].lower()

def normalize_jpg_suffix(suffix):
    """
        returns transform '.jpe' and '.jpeg' to '.jpg'
    """
    if suffix in ['.jpeg', '.jpe']:
        return '.jpg'
    return suffix
