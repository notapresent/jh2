# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Setting


class SettingManager(BaseManager):
    __model__ = Setting
