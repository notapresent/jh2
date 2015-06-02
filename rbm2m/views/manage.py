# -*- coding: utf-8 -*-
from flask import render_template, abort, url_for, Blueprint, current_app

from ..action import genre_manager, record_manager
from ..webapp import basic_auth, db
from ..models import record


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
    genman = genre_manager.GenreManager(db.session)
    genres = genman.all()
    return render_template('genre_list.html', genres=genres)


@bp.route('/records/')
def record_list():
    genman = genre_manager.GenreManager(db.session)
    genres = genman.all()
    return render_template('record_list.html', genres=genres)

@bp.route('/record/<int:rec_id>')
@bp.route('/record/', defaults={'rec_id': None})
def record_view(rec_id=None):
    recman = record_manager.RecordManager(db.session)
    rec = recman.get(rec_id)
    flag_names = [flag.name for flag in rec.flags]
    return render_template('record_view.html', record=rec, FLAGS=record.FLAGS,
                           flag_names=flag_names)
