# -*- coding: utf-8 -*-
"""
    Task entry points
"""
from sqlalchemy.exc import SQLAlchemyError
from action import scanner
from helpers import make_config, make_session, make_redis, setup_logging


config = make_config()
setup_logging(config.LOGS_DIR, 'worker', debug=config.DEBUG)
sess = make_session(None, config)
redis = make_redis(config)
scanner = scanner.Scanner(config, sess, redis)


def run_task(task_name, *args, **kwargs):

    method = getattr(scanner, task_name)
    try:
        method(*args, **kwargs)
    except SQLAlchemyError as e:
        sess.rollback()
        raise
    else:
        sess.commit()
    finally:
        sess.close()
