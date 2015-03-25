import re
import time
import logging

import requests
from bs4 import BeautifulSoup

from jh2.util import retry_on_exception

HOST = 'http://www.recordsbymail.com/'
# RESIZE_URL = '{host}php/resize.php?w={w}&h={h}&src={url}'
SEARCH_URL = '{host}search.php?genre={gst}&format=LP&instock=1&page={p}'
GENGE_LIST_URL = '{host}browse.php'
COUNT_URL = '{host}search.php?genre={st}&format={fmt}&instock={instock}'
TIMEOUTS = (3.05, 30)   # Connect, read

_logger = logging.getLogger(__name__)
details_rx = re.compile(r'Item #(\d+) \xb7 (.+) (LP|12|45)')


class ScrapeFailed(RuntimeError):
    pass


def scrape_page(genre_st, page_num):
    url = SEARCH_URL.format(host=HOST, gst=genre_st, p=page_num)
    try:
        html = fetch(url)
        return parse(html)

    except (requests.exceptions.RequestException) as e:
        raise ScrapeFailed(str(e))


@retry_on_exception()
def fetch(url):
    resp = requests.get(url, timeout=TIMEOUTS)
    return resp.text

def parse(html):
    soup = BeautifulSoup(html)
    container = soup.find('ul', id='records-list')
    items = container.find_all('li', class_ = 'record-block')
    results = []

    for i in items:
        results.append(parse_item(i))

    return results

def parse_item(i):
    # FIXME change &amp; to & (.decode_contents(formatter=None))
    img = i.find('meta', itemprop='image')
    details = i.find('div', class_='record-details-row').p.string
    oid, genre, fmt = details_rx.match(details).groups()
    tp = i.find('div', class_='record-details').p
    noteblock = i.find('p', class_='notes')
    price = i.find('span', class_='price').string.lstrip('$').replace(',','')
    rec = {
        'thumbnail': img.attrs['content'] if img else None,
        'oid': int(oid),
        'genre': flt_str(genre),
        'fmt': flt_str(fmt),
        'artist': flt_str(tp.a.string),
        'title': flt_str(tp.contents[1].strip(': ')),
        'label': flt_str(i.find('span', class_='label').string),
        'grade': flt_str(i.find('p', class_='grade').string),
        'price': int(price),
        'notes': flt_str(noteblock.string) if noteblock else None
    }

    return rec

def parse_genres():
    url = GENGE_LIST_URL.format(host=HOST)
    html = fetch(url)
    soup = BeautifulSoup(html)
    container = soup.find('div', class_=['content-box','single-col','browse-box']).ul
    items = container.find_all('li')
    genres = []
    for item in items:
        title = item.a.string.strip()
        search_term = title.split(u'&')[0].strip() if u'&' in title else title

        genres.append({
            'title': flt_str(title),
            'search_term': flt_str(search_term)
        })

    return genres

def count_records(genre_st, fmt='LP', instock=True):
    url = COUNT_URL.format(
        host=HOST,
        st=genre_st,
        fmt=fmt,
        instock=int(instock)
    )

    html = fetch(url)
    soup = BeautifulSoup(html)
    qtymsg = soup.find('p', class_=['results-count-text','right']).string
    return int(qtymsg.split(' ')[0].replace(',',''))

def flt_str(s):
    if s is None:
        return s

    return s.replace(u'\xa0', u' ').strip()
