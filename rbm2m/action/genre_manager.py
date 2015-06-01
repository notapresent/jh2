# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Genre


class GenreManager(BaseManager):
    __model__ = Genre
