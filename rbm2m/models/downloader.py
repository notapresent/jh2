# -*- coding: utf-8 -*-
import urllib

import requests


HOST = 'http://www.recordsbymail.com/'
GENRE_LIST_URL = '{host}browse.php'.format(host=HOST)
SEARCH_URL = '{host}search.php?genre={gt}&format=LP&instock=1&page={p}'
TIMEOUTS = (3.05, 30)   # Connect, read # TODO


def genre_list():
    return requests.get(GENRE_LIST_URL).content


def get_results_page(genre_title, page):
    url = SEARCH_URL.format(gt=urllib.quote_plus(genre_title), page=page)
    return requests.get(url).content
