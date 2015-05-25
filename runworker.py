# -*- coding: utf-8 -*-
import redis

from rq import Worker, Queue, Connection

from rbm2m.helpers import make_config

# TODO pre-import modules here


config = make_config()

listen = [config.RQ_QUEUE_NAME]
conn = redis.from_url(config.REDIS_URL)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
