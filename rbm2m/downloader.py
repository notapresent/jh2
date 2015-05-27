# -*- coding: utf-8 -*-
import urllib

import requests

HOST = 'http://www.recordsbymail.com/'
GENRE_LIST_URL = '{host}browse.php'.format(host=HOST)
SEARCH_URL = '{host}search.php?genre={genre_slug}&format=LP&instock=1'
IMAGE_LIST_URL = '{host}php/getImageArray.php?item={rec_id}'
TIMEOUTS = (3.05, 30)  # Connect, read # TODO


def fetch(url):
    """
        Download text content from url and return it.

        Raises `DownloadError` if operation fails
    """
    try:
        resp = requests.get(url, timeout=TIMEOUTS)
        resp.raise_for_status()
    except requests.RequestException as e:
        if resp.text:
            with open('dump.html', 'w') as f:
                f.write(resp.text)
        print "Failed url: {}".format(url)
        raise DownloadError(e)

    else:
        assert resp.text is not None
        return resp.text


def genre_list():
    """
        Download page with the list of genres
    """
    return fetch(GENRE_LIST_URL)


def get_results_page(genre_title, page):
    """
        Download search result page
    """
    url = SEARCH_URL.format(host=HOST,
                            genre_slug=urllib.quote_plus(genre_title))

    if page:
        url = url + '&page={}'.format(page)

    return fetch(url)


def get_image_list(rec_id):
    """
        Download list of images for a record
    """
    url = IMAGE_LIST_URL.format(host=HOST, rec_id=rec_id)
    return fetch(url)


class DownloadError(requests.RequestException):
    """
    Raised for all download errors (timeouts, http errors etc)
    """
    pass
