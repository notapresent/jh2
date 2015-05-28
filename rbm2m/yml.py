# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from sqlalchemy import func, or_
from jinja2.filters import do_truncate

from helpers import group_concat
from models import Scan, Record, Genre, RecordFlag, Image, scan_records


BATCH_SIZE = 10000

# TODO move this to settings
PRICE_FORMULA = 'x*60 if x < 1000 else x*60 + 10'

DESCRIPTION_TEMPLATE = '''
{artist} - {title}, {format}

Артикул товара:{id}
Лейбл: {label}
Грейд: {grade}
Примечания: {notes}

Дополнительный блок описания
'''


class Builder(object):
    def __init__(self, session):
        self.session = session

    def generation_date(self):
        """
            Returns catalog generation date
        """
        return datetime.datetime.utcnow()

    def genres_list(self):
        """
            Returns list of exported genres
        """
        return (
            self.session.query(Genre)
                .order_by(Genre.id)
                .filter(Genre.export_enabled.is_(True))
                .all()
        )

    def offers(self, limit=None):
        """
            Generates a sequence of offers for all records in exported genres
        """
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
            self.session.query(Scan.id).filter(Scan.status == 'success')
            .filter(Scan.genre_id == Genre.id).order_by(Scan.started_at.desc())
            .limit(1).as_scalar())
        rows = (
            self.session.query(Genre.id, subquery).filter(subquery.isnot(None))
            .all())
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
                self.session.query(scan_records.c.record_id.label('id'),
                    Record.artist, Record.title,
                    Record.label, Record.notes, Record.grade, Record.format,
                    Record.price, Genre.title.label('genre_title'),
                    func.group_concat(Image.source_url).label('images'))
                .join(Record, Record.id == scan_records.c.record_id)
                .join(Genre, Genre.id == Record.genre_id)
                .outerjoin(Image, Image.record_id == scan_records.c.record_id)
                .outerjoin(RecordFlag,
                           RecordFlag.record_id == scan_records.c.record_id)
                .filter(scan_records.c.scan_id.in_(scan_ids))
                .filter(or_(
                    RecordFlag.name.is_(None),
                    ~RecordFlag.name.in_(['skip', 'missing_images'])))
                .order_by(scan_records.c.record_id)
                .group_by(scan_records.c.record_id)
                .offset(batch_no * BATCH_SIZE).limit(BATCH_SIZE).all())

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

    return offer


def format_title(artist, title, fmt, max_length=50):
    """
        Format offer title string according to format
        {artist} - {title} {format}
        truncating title if necessary
    """
    title_maxlength = max_length - len("{} -  {}".format(artist, fmt))
    truncated_title = do_truncate(title, title_maxlength)
    return '{} - {} {}'.format(artist, truncated_title, fmt)
