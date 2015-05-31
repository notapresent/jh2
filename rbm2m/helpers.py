# -*- coding: utf-8 -*-
import os
import time
from functools import wraps

from redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.ext import compiler
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression
from sqlalchemy.exc import SQLAlchemyError

from . import config


def make_engine(cfg=None):
    if not cfg:
        cfg = make_config()

    return create_engine(
        cfg.SQLALCHEMY_DATABASE_URI,
        echo=cfg.SQLALCHEMY_ECHO,
    )


def make_session(engine=None, config=None):
    if not engine:
        engine = make_engine(config)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def make_config(app_env=None):
    if app_env is None:
        app_env = os.environ.get('RBM2M_ENV', 'Production')
    return getattr(config, '{}Config'.format(app_env))


def make_redis(redis_url):
    return StrictRedis.from_url(redis_url)


def retry(exception_to_check, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exception_to_check: the exception to check. may be a tuple of
        exceptions to check
    :type exception_to_check: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


class group_concat(expression.FunctionElement):
    """
        Custom function for use with SQLAlchemy
    """
    name = "group_concat"


@compiler.compiles(group_concat, 'mysql')
def _group_concat_mysql(element, compilr, **kw):
    if len(element.clauses) == 2:
        separator = compilr.process(element.clauses.clauses[1])
    else:
        separator = ','

    return 'GROUP_CONCAT(%s SEPARATOR %s)'.format(
        compilr.process(element.clauses.clauses[0]), separator, )


def run_job(job, *args, **kwargs):
    job.config = make_config()
    session = make_session()
    job.session = session

    try:
        job.run(*args, **kwargs)
    except SQLAlchemyError:
        session.rollback()
    else:
        session.commit()
    finally:
        session.close()
