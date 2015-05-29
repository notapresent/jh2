# -*- coding: utf-8 -*-
from rbm2m.helpers import retry
from rbm2m.action import parser, downloader


class ScrapeError(Exception):
    """
    Raised if scraping failed for any reason (after all retries)
    """
    pass


@retry(ScrapeError, tries=4, delay=30, backoff=2)
def scrape_page(genre_title, page):
    """
    Download search results page and extract records, total number of records
    and next page

    :param genre_title:
    :param page:
    :return: tuple (records, total_record_count, next_page)
    """
    try:
        html = downloader.get_results_page(genre_title, page)
        return parser.parse_page(html)
    except (downloader.DownloadError, parser.ParseError) as e:
        raise ScrapeError(str(e))


@retry(ScrapeError, tries=2, delay=5)
def genre_list():
    """
    Downloads genre list from site, parses it and returns list of genre titles

    :returns list of genre titles
    """
    try:
        html = downloader.genre_list()
        return parser.parse_genres(html)
    except (downloader.DownloadError, parser.ParseError) as e:
        raise ScrapeError(str(e))


@retry(ScrapeError, tries=2, delay=5)
def image_list(rec_id):
    """
        Downloads list of images for a record
    """
    try:
        json = downloader.get_image_list(rec_id)
        return parser.parse_image_list(json)
    except (downloader.DownloadError, parser.ParseError) as e:
        raise ScrapeError(str(e))


def get_image_urls(rec_ids):
    """
        Download image urls for all records in rec_ids
    """
    pass


