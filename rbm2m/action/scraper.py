# -*- coding: utf-8 -*-
from rbm2m.helpers import retry
import rbm_parser
import downloader


class ScrapeError(Exception):
    """
        Raised if scraping failed for any reason (after all retries)
    """
    pass


class Scrape(object):
    """
        Represents one page scrape operation
    """
    def __init__(self):
        self.records = []
        self.next_page = None
        self.rec_count = None

    @retry(ScrapeError, tries=4, delay=30, backoff=2)
    def run(self, genre_title, page):
        """
            Download search results page and extract records, total number of
            records and next page
        """
        try:
            html = downloader.get_results_page(genre_title, page)
            rv = rbm_parser.parse_page(html)
        except (downloader.DownloadError, rbm_parser.ParseError) as e:
            raise ScrapeError(str(e))
        else:
            self.records, self.next_page, self.rec_count = rv


@retry(ScrapeError, tries=2, delay=5)
def genre_list():
    """
        Download and parse genre list rom rbm
    """
    try:
        html = downloader.genre_list()
        return rbm_parser.parse_genres(html)
    except (downloader.DownloadError, rbm_parser.ParseError) as e:
        raise ScrapeError(str(e))


@retry(ScrapeError, tries=2, delay=5)
def image_list(rec_id):
    """
        Downloads list of images for a record
    """
    try:
        json_data = downloader.get_image_list(rec_id)
        return rbm_parser.parse_image_list(json_data)
    except (downloader.DownloadError, rbm_parser.ParseError) as e:
        raise ScrapeError(str(e))


def get_image_urls(rec_ids):
    """
        Download image urls for all records in rec_ids
    """
    pass


