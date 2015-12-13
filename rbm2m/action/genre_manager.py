# -*- coding: utf-8 -*-
from base_manager import BaseManager
from . import scraper
from ..models import Genre


class GenreManager(BaseManager):
    __model__ = Genre

    def exported_list(self):
        return (
            self.session.query(Genre)
            .filter(Genre.export_enabled.is_(True))
            .order_by(Genre.id)
        )

    def import_genres(self):
        """
          Import genres from rbm2m
        """
        for genre_title in scraper.genre_list():
            self.session.add(Genre(title=genre_title))
