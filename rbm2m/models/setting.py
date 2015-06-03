# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from .base import Base


class Setting(Base):
    __tablename__ = 'settings'

    name = Column(String(32), nullable=False, primary_key=True)
    value = Column(String(512), nullable=False)
    description = Column(String(512))
