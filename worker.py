# -*- coding: utf-8 -*-
import os

import redis
from rq import Worker, Queue, Connection

import rbm2m.config


app_env = os.environ.get('RBM2M_ENV', 'Production')
config = getattr(rbm2m.config, 'Config'.format(app_env))

listen = ['default']
conn = redis.from_url(config.REDIS_URI)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
