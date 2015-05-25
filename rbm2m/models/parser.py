# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from rbm2m.util import to_unicode


def parse_genres(html):
    soup = BeautifulSoup(html)
    div = soup.find('div', class_=['content-box', 'single-col', 'browse-box'])
    items = div.ul.find_all('li')

    for item in items:
        yield to_unicode(item.a.text).strip()


def parse_page(html):
    soup = BeautifulSoup(html)
    # TODO
    return [], False, -1