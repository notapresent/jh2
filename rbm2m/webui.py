# -*- coding: utf-8 -*-
from flask import Flask
from rbm2m import config


app = Flask(__name__)
app.config.from_object('rbm2m.config.{}Config'.format(config.get_app_env()))

@app.route("/")
def hello():
    return "Hello World!"


