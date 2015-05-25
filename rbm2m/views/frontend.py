# -*- coding: utf-8 -*-
from flask import render_template, abort, url_for, Blueprint, current_app

from rbm2m import basic_auth, db
bp = Blueprint('frontend', __name__)


@bp.before_request
def check_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


@bp.route('/')
def home():
    return render_template('dashboard.html')
