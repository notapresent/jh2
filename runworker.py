# -*- coding: utf-8 -*-
import os

app_env = os.environ.get('RBM2M_ENV', 'Production')

if app_env == 'Production':
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    activate_this = os.path.join(venv_path, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))


import redis
from rq import Worker, Queue, Connection

from rbm2m.helpers import make_config

config = make_config()
listen = [config.RQ_QUEUE_NAME]
conn = redis.from_url(config.REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
