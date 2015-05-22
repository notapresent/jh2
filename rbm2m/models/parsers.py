# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from rbm2m.util import to_unicode


def parse_genres(html):
    soup = BeautifulSoup(html)
    container = soup.find('div', class_=['content-box', 'single-col', 'browse-box']).ul
    items = container.find_all('li')
    for item in items:
        yield to_unicode(item.a.text).strip()
