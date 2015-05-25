# -*- coding: utf-8 -*-
from . import Genre, scraper


# TODO refactor this
class GenreManager(object):
    @staticmethod
    def import_genres(session):

        for title in scraper.genre_list():
            session.add(Genre(title=title))
        session.commit()
