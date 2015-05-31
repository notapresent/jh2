# -*- coding: utf-8 -*-
from flask import render_template, abort, url_for, Blueprint, current_app

from ..models import Genre
from ..webapp import basic_auth, db

bp = Blueprint('manage', __name__)


@bp.before_request
def check_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


@bp.route('/')
def home():
    return render_template('dashboard.html')


@bp.route('/genre/')
def genre_list():
    genres = db.session.query(Genre).order_by(Genre.id).all()
    return render_template('genre_list.html', genres=genres)
