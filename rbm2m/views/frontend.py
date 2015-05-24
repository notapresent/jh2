# -*- coding: utf-8 -*-
from flask import render_template, abort, url_for, Blueprint

from rbm2m import basic_auth


bp = Blueprint('frontend', __name__)


@bp.route('/')
@basic_auth.required
def home():
    return render_template('dashboard.html')
