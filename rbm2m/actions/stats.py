# -*- coding: utf-8 -*-
from sqlalchemy import func, distinct
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import literal
from ..models import Record, Image, Scan, Genre, scan_records


def get_overview(sess):
    """
        Returns aggregated statistics about records, scans, genres etc
    """
    last_scan_ids = [scan.id for scan in last_scans(sess)]

    if not last_scan_ids:       # Append dummy ID to avoid SA warning
        last_scan_ids = [-1]    # about IN-predicate with an empty sequence

    rec_instock = (
        sess.query(func.count(distinct(scan_records.c.record_id)))
        .filter(scan_records.c.scan_id.in_(last_scan_ids))
        .as_scalar()
    )

    img_total = sess.query(func.count(Image.id)).as_scalar()
    img_total_size = sess.query(func.sum(Image.length)).as_scalar()

    lots = (
        sess.query(func.count(scan_records.c.record_id))
        .filter(scan_records.c.scan_id.in_(last_scan_ids))
        .join(Scan)
        .join(Genre)
        .filter(Genre.export_enabled.is_(True))
        .as_scalar()
    )

    row = sess.query(
        func.count(Record.id).label('records_total'),
        rec_instock.label('records_in_stock'),
        img_total.label('images_total'),
        img_total_size.label('images_total_length'),
        lots.label('lots')
    ).one()

    result = dict(zip(row.keys(), row))

    result['images_total_length'] = int(result['images_total_length'])

    return result


def last_scans(sess):
    """
        Returns list of last successful scans, one for each genre
    """
    s1 = aliased(Scan)
    rows = (
        sess.query(Scan)
            .join(Genre, Scan.genre_id == Genre.id)
            .filter(Scan.id == sess.query(s1.id)
                    .filter(s1.genre_id == Genre.id)
                    .filter(s1.status == 'success')
                    .order_by(s1.started_at.desc())
                    .limit(1)
                    .as_scalar()
                    )
            .all()
    )
    return rows

def active_scans(sess):
    """
        Returns list of scans currently in progress, along with
        current record count for each scan
    """
    rec_count = (
        sess.query(func.count(scan_records.c.record_id))
            .filter(scan_records.c.scan_id == Scan.id)
            .correlate(Scan)
            .as_scalar()
    )
    rows = (
        sess.query(Scan.id, Scan.started_at, Scan.est_num_records,
                   rec_count.label('num_records'), Genre.title)
            .join(Genre, Genre.id == Scan.genre_id)
            .filter(Scan.status == 'started')
            .order_by(Scan.started_at)
            .all()
    )

    scans = [dict(zip(r.keys(), r)) for r in rows]
    return scans
