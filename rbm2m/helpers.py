# -*- coding: utf-8 -*-
import os
import time
from functools import wraps
import re
from unicodedata import normalize
import logging
import logging.config
from logging import StreamHandler, Formatter
from logging.handlers import RotatingFileHandler



from redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.ext import compiler
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression
from sqlalchemy.exc import SQLAlchemyError
from flask.json import JSONEncoder as BaseJSONEncoder

from . import config
from .util import to_unicode


logger = logging.getLogger(__name__)


def make_engine(cfg=None):
    if not cfg:
        cfg = make_config()

    return create_engine(
        cfg.SQLALCHEMY_DATABASE_URI,
        echo=cfg.SQLALCHEMY_ECHO,
    )


def make_session(engine=None, cfg=None):
    if not engine:
        engine = make_engine(cfg)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def make_config(app_env=None):
    if app_env is None:
        app_env = os.environ.get('RBM2M_ENV', 'Production')
    return getattr(config, '{}Config'.format(app_env))


def make_redis(config):
    return StrictRedis.from_url(config.REDIS_URL)


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


class JsonSerializer(object):

    """A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON serializer.
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv


class JSONEncoder(BaseJSONEncoder):

    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """

    def default(self, obj):
        if isinstance(obj, JsonSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)



_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(to_unicode(text.lower())):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def setup_logging(log_dir, component, debug=True):
    applogger = logging.getLogger('rbm2m')

    if debug:
        applogger.setLevel(logging.DEBUG)
        hnd = StreamHandler()
        hnd.setFormatter(Formatter(
            '%(name)s %(levelname)s: %(message)s'
        ))
        applogger.addHandler(hnd)

    else:
        applogger.setLevel(logging.WARNING)
        filename = os.path.join(log_dir, '{}.log'.format(component))
        hnd = RotatingFileHandler(filename, maxBytes=5000000, backupCount=5)
        hnd.setFormatter(Formatter(
            '%(asctime)s %(process)d %(name)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        applogger.addHandler(hnd)

    # Limit 3rd party package logging
    loggers = ['requests', 'sqlalchemy', 'rq']
    for logger_name in loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
