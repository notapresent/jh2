# -*- coding: utf-8 -*-
"""
    Task entry points
"""
from sqlalchemy.exc import SQLAlchemyError
from action import scanner
from helpers import make_config, make_session, make_redis


config = make_config()
sess = make_session(config)
redis = make_redis(config)
scanner = scanner.Scanner(config, sess, redis)


def run_task(task_name, *args, **kwargs):

    method = getattr(scanner, task_name)
    try:
        method(*args, **kwargs)
    except SQLAlchemyError as e:
        sess.rollback()
    else:
        sess.commit()
    finally:
        sess.close()
