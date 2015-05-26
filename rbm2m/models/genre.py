# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, String, Boolean)

from .base import Base


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    import_enabled = Column(Boolean(), nullable=False, default=False)
    export_enabled = Column(Boolean(), nullable=False, default=False)
