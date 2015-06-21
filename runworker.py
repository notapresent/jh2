# -*- coding: utf-8 -*-
import os


base_dir = os.path.dirname(__file__)
venv_path = os.path.join(base_dir, 'venv')

app_env = os.environ.get('RBM2M_ENV', 'Production')

if app_env == 'Production' and os.path.isdir(venv_path):
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
