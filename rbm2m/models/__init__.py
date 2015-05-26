# -*- coding: utf-8 -*-
"""
    This package contains SQLAlchemy model classes
"""

from .genre import Genre
from .image import Image
from .record import Record, RecordStatus
from .scan import Scan, ScanRecord

# This allows `from models import *` for simple create_all/drop_all
__all__ = ['Genre', 'Image', 'Record', 'RecordStatus', 'Scan', 'ScanRecord']
