# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from .base import Base


class Setting(Base):
    __tablename__ = 'settings'

    name = Column(String(32), nullable=False, primary_key=True)
    value = Column(String(512))
    default_value = Column(String(512))
    title = Column(String(127), nullable=False)
    data_type = Column(String(8))   # string or text for now
    description = Column(String(512))
