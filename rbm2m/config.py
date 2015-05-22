# -*- coding: utf-8 -*-
import os


def get_app_env():
    return os.environ.get('RBM2M_ENV', 'Production')


class Config(object):
    APP_ENV = get_app_env()
    DEBUG = False
    TESTING = False
    # TODO: ?charset=utf8
    DATABASE_URI = 'mysql://rbm2m:rbm2m@localhost/rbm2m'
    REDIS_URI = 'redis://@localhost:6379/0'


class ProductionConfig(Config):
    DATABASE_URI = os.environ.get('RBM2M_DATABASE_URI')
    REDIS_URI = os.environ.get('RBM2M_REDIS_URI')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'mysql://rbm2m:rbm2m@localhost/rbm2m_test'
