# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from sqlalchemy import func, or_
from sqlalchemy.sql import expression
from jinja2.filters import do_truncate

from helpers import group_concat
from models import Scan, Record, ScanRecord, Genre, RecordStatus, Image


# TODO
CATEGORIES = [
    {'id': 1, 'title': 'Музыка'},
    {'id': 2, 'title': 'Пластинки', 'parent_id': 1}
]

BATCH_SIZE = 10000

# TODO move this to setings
PRICE_FORMULA = 'x*60 if x < 1000 else x*60 + 10'

DESCRIPTION_TEMPLATE = '''
{artist} - {title}, {format}
{id}
{label}
{grade}
{notes}
Это дополнительный блок описания
'''


class Builder(object):
    def __init__(self, session):
        self.session = session

    def build(self, limit=None):
        result = {
            'generation_date': datetime.datetime.utcnow(),
            'categories': CATEGORIES,
            'offers': self.offers(limit=limit)
        }
        return result

    def offers(self, limit):
        scans = self.latest_scans()

        for num, rec in enumerate(self.records(scans)):
            if limit and num == limit:
                break
            else:
                yield make_offer(rec)

    def latest_scans(self):
        """
            Returns list of ids of last successful scans for each
            export-enabled genre
        """
        subquery = (
            self.session.query(Scan.id)
                .filter(Scan.status == 'success')
                .filter(Scan.genre_id == Genre.id)
                .order_by(Scan.started_at.desc())
                .limit(1)
                .as_scalar()
        )
        rows = (
            self.session.query(Genre.id, subquery)
                .filter(subquery.isnot(None))
                .all()
        )
        return [scan_id for genre_id, scan_id in rows]

    def records(self, scan_ids):
        """
            Returns all records from scans in scan_ids, excluding the ones with
            'sold' and 'skip' status

            :param scan_ids: list of scan ids
            :return: generator producing Record values
        """
        batch_no = 0
        while True:
            records = (
                self.session.query(
                    ScanRecord.scan_id,
                    Record.id, Record.artist, Record.title, Record.label,
                    Record.notes, Record.grade, Record.format, Record.price,
                    Genre.title.label('genre_title'),
                    func.group_concat(Image.source_url).label('images')
                )

                .join(Record, Record.id == ScanRecord.record_id)
                .join(Genre, Genre.id == Record.genre_id)
                .outerjoin(Image, Image.record_id == ScanRecord.record_id)
                .outerjoin(RecordStatus,
                           RecordStatus.record_id == ScanRecord.record_id)

                .filter(ScanRecord.scan_id.in_(scan_ids))
                .filter(or_(
                    RecordStatus.status.is_(None),
                    ~RecordStatus.status.in_(['sold', 'skip'])
                ))

                .order_by(ScanRecord.record_id)
                .group_by(ScanRecord.record_id)
                .offset(batch_no * BATCH_SIZE)
                .limit(BATCH_SIZE)
                .all()
            )

            if not records:
                break

            for row in records:
                yield dict(zip(row.keys(), row))

            batch_no += 1

def make_offer(rec):
    """
        Generates offer for YML from result row dictionary
    """
    offer = rec.copy()
    offer['title'] = format_title(rec['artist'], rec['title'], rec['format'])
    offer['description'] = DESCRIPTION_TEMPLATE.format(**rec)
    offer['price'] = eval(PRICE_FORMULA, {'x': rec['price']})
    offer['images'] = rec['images'].split(',') if rec['images'] else []
    offer['category'] = 1   # TODO

    return offer


def format_title(artist, title, format, max_length=50):
    """
        Format offer title string according to format
        {artist} - {title} {format}
        truncating title if necessary
    """
    title_maxlength = max_length - len("{} -  {}".format(artist, format))
    truncated_title = do_truncate(title, title_maxlength)
    return '{} - {} {}'.format(artist, truncated_title, format)
