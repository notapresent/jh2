# -*- coding: utf-8 -*-
"""
    Task entry points
"""
from redis import StrictRedis

from rbm2m.action import taskman
from rbm2m.helpers import make_session, make_config, make_engine


def run_task(task_name, *args, **kwargs):
    config = make_config()
    session = make_session(engine=make_engine(config))
    redis_conn = StrictRedis.from_url(config.REDIS_URL)

    tm = taskman.TaskManager(config=config, session=session, redis=redis_conn)

    # TODO scoped session with commit/rollback here
    tm.run_task(task_name, *args, **kwargs)
