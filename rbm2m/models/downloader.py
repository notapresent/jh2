# -*- coding: utf-8 -*-
import urllib

import requests


HOST = 'http://www.recordsbymail.com/'
GENRE_LIST_URL = '{host}browse.php'.format(host=HOST)
SEARCH_URL = '{host}search.php?genre={genre_slug}&format=LP&instock=1&page={page}'
TIMEOUTS = (3.05, 30)   # Connect, read # TODO


def genre_list():
    try:
        return requests.get(GENRE_LIST_URL).content
    except requests.RequestException as e:
        DownloadError(e)


def get_results_page(genre_title, page):
    url = SEARCH_URL.format(host=HOST, genre_slug=urllib.quote_plus(genre_title), page=page)

    try:
        return requests.get(url).content
    except requests.RequestException as e:
        DownloadError(e)


class DownloadError(requests.RequestException):
    """
    Raised for all download errors (timeouts, http errors etc)
    """
    pass
