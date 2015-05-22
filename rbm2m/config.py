# -*- coding: utf-8 -*-
import os


app_environment = os.environ.get('RBM2M_ENV', 'Production')


class Config(object):
    APP_ENV = app_environment
    DEBUG = False
    TESTING = False
    # TODO: ?charset=utf8
    REDIS_URI = 'redis://@localhost:6379/0'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('RBM2M_DATABASE_URI')
    REDIS_URI = os.environ.get('RBM2M_REDIS_URI')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://rbm2m:rbm2m@127.0.0.1/rbm2m'
    SQLALCHEMY_ECHO = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://rbm2m:rbm2m@localhost/rbm2m_test'
