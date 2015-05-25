# -*- coding: utf-8 -*-
from flask import render_template, abort, url_for, Blueprint, current_app

from .. import webapp


bp = Blueprint('frontend', __name__)


@bp.before_request
def check_auth():
    if not webapp.basic_auth.authenticate():
        return webapp.basic_auth.challenge()


@bp.route('/')
def home():
    return render_template('dashboard.html')
