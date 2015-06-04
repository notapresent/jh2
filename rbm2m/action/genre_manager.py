# -*- coding: utf-8 -*-
from base_manager import BaseManager
from ..models import Genre


class GenreManager(BaseManager):
    __model__ = Genre

    def exported_list(self):
        return (
            self.session.query(Genre)
            .filter(Genre.export_enabled.is_(True))
            .order_by(Genre.id)
        )
