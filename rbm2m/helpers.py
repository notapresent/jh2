# -*- coding: utf-8 -*-
import os
import time
from functools import wraps

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from .import config
from models.record import Record
from models.image import Image


def make_engine(cfg):
    return create_engine(
        cfg.SQLALCHEMY_DATABASE_URI,
        echo=cfg.SQLALCHEMY_ECHO,
        # client_encoding='utf8'    # TODO
    )


def make_session(engine=None):
    Session = sessionmaker(bind=engine)
    session = Session()
    # For Flask-SQLAlchemy models   # TODO DO we need it here?
    session._model_changes = {}
    return session


def make_config(app_env=None):
    if app_env is None:
        app_env = os.environ.get('RBM2M_ENV', 'Production')
    return getattr(config, '{}Config'.format(app_env))


def get_stats(session):
    return {
        'records_total': session.query(func.count(Record.id)).scalar(),
        # Number of records in last successful crawl for each genre
        'records_in_stock': -1,
        'images_total': session.query(func.count(Image.id)).scalar(),
        # Number of records in last successful crawl for each exported genre
        'lots': -1,
        # number of failed crawls, at most one for each genre
        'errors': -1
    }


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
