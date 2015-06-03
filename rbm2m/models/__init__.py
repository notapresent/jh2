# -*- coding: utf-8 -*-
"""
    This package contains SQLAlchemy model classes
"""

from .genre import Genre
from .image import Image
from .record import Record, RecordFlag
from .scan import Scan, scan_records
from .export import Export
from setting import Setting


# This allows `from models import *` for simple create_all/drop_all
__all__ = ['Genre', 'Image', 'Record', 'RecordFlag', 'Scan', 'scan_records',
           'Export', 'Setting']
