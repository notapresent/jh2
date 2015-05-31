# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Image


class ImageManager(BaseManager):
    __class__ = Image
