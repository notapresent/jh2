# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Config(object):
    """
        Default configuration
    """
    DEBUG = False
    TESTING = False
    REDIS_URL = 'redis://@localhost:6379/0'
    RQ_QUEUE_NAME = 'default'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://rbm2m:rbm2m@127.0.0.1/rbm2m?charset=utf8'    # noqa
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    BASIC_AUTH_USERNAME = os.environ['RBM2M_LOGIN']
    BASIC_AUTH_PASSWORD = os.environ['RBM2M_PASSWORD']

    MEDIA_DIR = os.path.join(BASE_DIR, 'media')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('RBM2M_DATABASE_URI')
    REDIS_URL = os.environ.get('RBM2M_REDIS_URI')


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://rbm2m:rbm2m@localhost/rbm2m_test?charset=utf8'  # noqa
