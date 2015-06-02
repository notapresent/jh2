# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import (Column, Integer, String, DateTime)

from .base import Base


class Export(Base):
    __tablename__ = 'exports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    format = Column(String(5), nullable=False, default='yml')
    started_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    ip = Column(String(26), nullable=False)
    user_agent = Column(String(500), nullable=False)
