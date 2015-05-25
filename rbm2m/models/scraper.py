# -*- coding: utf-8 -*-
from . import downloader, parser


def scrape_page(genre_title, page):
    html = downloader.get_results_page(genre_title, page)
    return parser.parse_page(html)


def genre_list():
    """
    Downloads genre list from site, parses it and returns list of genre titles

    :returns list
    """
    html = downloader.genre_list()
    return parser.parse_genres(html)
