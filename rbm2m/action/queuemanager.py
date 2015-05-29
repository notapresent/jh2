# -*- coding: utf-8 -*-
import rq

from ..helpers import make_redis, run_job


JOB_TIMEOUT = 300


class QueueManager(object):
    def __init__(self, config, redis=None):
        self.config = config
        self.redis = redis or make_redis(config.REDIS_URL)
        self.q = rq.Queue(default_timeout=JOB_TIMEOUT, connection=redis)

    def enqueue(self, *args, **kwargs):
        return self.q.enqueue(run_job, *args, **kwargs)

