# -*- coding: utf-8 -*-
import sys
import urlparse
import json

import bs4

from rbm2m.util import to_unicode
from .debug import dump_exception


def parse_genres(html):
    soup = bs4.BeautifulSoup(html)
    div = soup.find('div', class_=['content-box', 'single-col', 'browse-box'])
    items = div.ul.find_all('li')

    for item in items:
        yield to_unicode(item.a.text).strip().strip(';')


def parse_page(html):
    try:
        soup = bs4.BeautifulSoup(html)
        records = list(extract_records(soup))
        next_page = extract_next_page(soup)
        total_count = extract_total_count(soup)

    except Exception as e:
        exc_type, exc_val, tb = sys.exc_info()
        dump_exception('parse_page', exc_type, exc_val, tb, html)
        raise ParseError(e)

    else:
        return records, next_page, total_count


def parse_image_list(json_data):
    try:
        urls = json.loads(json_data)
        return list(set(urls))
    except ValueError as e:
        raise ParseError(e)


def extract_records(soup):
    """
        Extract records from search page result, represented by BS object
        Yields successfully parsed records as dicts
    """
    container = soup.find('ul', id='records-list')
    items = container.find_all('li', class_='record-block')

    for item in items:
        try:
            yield parse_record_block(item)
        except RecordParseFailed:
            exc_type, exc_val, tb = sys.exc_info()
            dump_exception('parse_record', exc_type, exc_val, tb, str(item))


def parse_record_block(tag):
    """
        Parse tag containing record and return parsed values as a dict
    """
    try:
        rec = {
            'id': int(tag.attrs['id']),
            'artist': extract_artist(tag),
            'title': extract_title(tag),
            'label': extract_label(tag),
            'notes': extract_notes(tag),
            'grade': extract_grade(tag),
            'price': extract_price(tag),
            'format': extract_format(tag),
            'has_images': has_images(tag),
        }
    except Exception as e:
        raise RecordParseFailed(str(e))
    else:
        return rec


def has_images(tag):
    return tag.find('meta', itemprop='image') is not None


def extract_artist(tag):
    return tag.find('div', class_='record-details').p.a.text


def extract_title(tag):
    raw_title = tag.find('div', class_='record-details').p.contents[1]
    return raw_title.strip(': ')


def extract_label(tag):
    return tag.find('span', class_='label').text


def extract_grade(tag):
    return tag.find('p', class_='grade').text


def extract_price(tag):
    price_text = tag.find('span', class_='price').text
    price_text = price_text.replace(',', '')
    return int(price_text.strip('$'))


def extract_notes(tag):
    notes_tag = tag.find('p', class_='notes')
    return notes_tag.text if notes_tag else None


def extract_format(tag):
    details = tag.find('div', class_='record-details-row').p.string
    return details.split(' ')[-1]


def extract_next_page(soup):
    pagination = soup.find('div', class_='paging-box')
    last_link = pagination.find_all('a')[-1]

    if last_link.text != 'Next':
        return None

    return href_to_page(last_link.attrs['href'])


def href_to_page(href):
    """
        Extracts page number from 'Next page' link
    """
    params = dict(urlparse.parse_qsl(href))
    return int(params.get('page', 0))


def extract_total_count(soup):
    count_text = soup.find('p', class_='results-count-text').text
    return int(count_text.split(' ')[0])


class ParseError(Exception):

    """
        Raised for all parse errors.
    """
    pass


class RecordParseFailed(ParseError):

    """
        Raised if parsing particular record failed
    """
    pass
