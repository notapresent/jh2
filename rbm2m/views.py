# -*- coding: utf-8 -*-
from flask import render_template, abort, url_for, Blueprint

from . import basic_auth


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@basic_auth.required
def home():
    return render_template('dashboard.html')
