# -*- coding: utf-8 -*-
import datetime

from rbm2m.models.db import Scan


def start_scan(genre_id):
    if current_scan(genre_id):
        raise AlreadyStartedException('Scan for genre #%d already started'
                                      % genre_id)

    scan = Scan(
        genre_id=genre_id,
        started_at=datetime.datetime.utcnow(),
        status='started'
    )


def abort_scan():
    pass


def current_scan(genre_id):
    return Scan.query.filter_by(genre_id=genre_id, status='started').first()


class AlreadyStartedException(RuntimeWarning):
    pass
