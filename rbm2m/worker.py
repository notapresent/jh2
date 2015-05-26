# -*- coding: utf-8 -*-
from redis import StrictRedis

from rbm2m.models.scheduler import Scheduler
from rbm2m.helpers import make_session, make_config, make_engine


config = make_config()
session = make_session(engine=make_engine(config))
redis_conn = StrictRedis.from_url(config.REDIS_URL)

scheduler = Scheduler(session, redis_conn, config.RQ_QUEUE_NAME)

# TODO: Refactor this atrocity
def start_scan(genre_id):
    scheduler.start_scan(genre_id)


def finish_scan(scan_dict, pages, status):
    scheduler.finish_scan(scan_dict, pages, status)


def task(scan_id, page=0):
    scheduler.run_task(scan_id, page)


def abort_scan(scan_id):
    scheduler.abort_scan(scan_id)
