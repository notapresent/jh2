# -*- coding: utf-8 -*-
from rbm2m.models.db import Genre
from rbm2m.models.parsers import parse_genres
from rbm2m.models.downloader import Downloader


class GenreManager(object):
    @staticmethod
    def import_genres(session):
        html = Downloader.get_genre_list()
        for title in parse_genres(html):
            session.add(Genre(title=title))
        session.commit()
