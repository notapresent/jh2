# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, String, Boolean)

from .base import Base


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    import_active = Column(Boolean(), nullable=False, default=False)
    export_active = Column(Boolean(), nullable=False, default=False)
