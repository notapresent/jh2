# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from rbm2m.util import to_unicode


def parse_genres(html):
    soup = BeautifulSoup(html)
    lst = soup.find('div', class_=['content-box', 'single-col', 'browse-box']).ul
    items = lst.find_all('li')
    for item in items:
        yield to_unicode(item.a.text).strip()

def get_num_pages(html):
    pass