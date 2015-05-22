# -*- coding: utf-8 -*-
import requests


HOST = 'http://www.recordsbymail.com/'
GENRE_LIST_URL = '{host}browse.php'.format(host=HOST)
SEARCH_URL = '{host}search.php?genre={gst}&format=LP&instock=1&page={p}'
# RESIZE_URL = '{host}php/resize.php?w={w}&h={h}&src={url}'
COUNT_URL = '{host}search.php?genre={st}&format={fmt}&instock={instock}'
TIMEOUTS = (3.05, 30)   # Connect, read


class Downloader(object):
    @staticmethod
    def get_genre_list():
        return requests.get(GENRE_LIST_URL).content
