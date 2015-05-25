# -*- coding: utf-8 -*-
import datetime

from rq import Queue

from rbm2m.models.db import Scan


def start_scan(genre_id, sess):
    if current_scan(genre_id):
        raise AlreadyStarted('Scan for genre #%d already started' % genre_id)

    scan = Scan(
        genre_id=genre_id,
        started_at=datetime.datetime.utcnow(),
        status='started'
    )
    sess.add(scan)
    sess.commit()
    # Enqueue job here

    return scan

def abort_scan(scan_id):
    pass


def current_scan(genre_id):
    return Scan.query.filter_by(genre_id=genre_id, status='started').first()


class ScheduleError(Exception):
    pass

class AlreadyStarted(ScheduleError):
    pass
