# -*- coding: utf-8 -*-
"""
    Flask app initialization
"""

from flask import Flask
from flask.ext.basicauth import BasicAuth
from flask.ext.redis import FlaskRedis
from flask.ext.sqlalchemy import SQLAlchemy

from helpers import JSONEncoder, setup_logging

db = SQLAlchemy()
basic_auth = BasicAuth()
redis = FlaskRedis()


def create_app(app_env):
    app = Flask(__name__)
    app.config.from_object('rbm2m.config.{}Config'.format(app_env))
    setup_logging(app.config['LOGS_DIR'], 'web', app.debug)
    app.json_encoder = JSONEncoder
    db.init_app(app)
    basic_auth.init_app(app)
    redis.init_app(app, strict=True)

    from rbm2m.views import manage, api, public
    app.register_blueprint(manage.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(public.bp, url_prefix='/public')
    return app
