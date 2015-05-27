# -*- coding: utf-8 -*-
"""
    Flask app initialization
"""

from flask import Flask
from flask.ext.basicauth import BasicAuth
from flask.ext.redis import FlaskRedis
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
basic_auth = BasicAuth()
redis = FlaskRedis()


def create_app(app_env):
    app = Flask(__name__)
    app.config.from_object('rbm2m.config.{}Config'.format(app_env))

    db.init_app(app)
    basic_auth.init_app(app)
    redis.init_app(app, strict=True)

    # TODO rename `frontend` to `manage`
    from rbm2m.views import frontend, api, public
    app.register_blueprint(frontend.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(public.bp, url_prefix='/public')
    return app
