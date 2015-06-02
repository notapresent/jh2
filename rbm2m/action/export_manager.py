# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Export


class ExportManager(BaseManager):
    __model__ = Export
