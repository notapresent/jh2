# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from rbm2m import config
from rbm2m.views import webui


__version__ = '0.3'


db = SQLAlchemy()


def create_app(app_env):
    app = Flask(__name__)
    app.config.from_object('rbm2m.config.{}Config'.format(app_env))
    db.init_app(app)
    app.register_blueprint(webui)
    return app
