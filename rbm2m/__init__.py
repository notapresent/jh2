# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.basicauth import BasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

from rbm2m import config

__version__ = '0.3'


db = SQLAlchemy()
basic_auth = BasicAuth()

def create_app(app_env):
    app = Flask(__name__)
    app.config.from_object('rbm2m.config.{}Config'.format(app_env))

    # from rbm2m.models.db import *

    db.init_app(app)
    basic_auth.init_app(app)
    from rbm2m.views import frontend
    app.register_blueprint(frontend)

    return app


