# -*- coding: utf-8 -*-
import os

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
        os.environ.get('RBM2M_ENV', 'Production')
    return getattr(config, 'Config'.format(app_env))


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


