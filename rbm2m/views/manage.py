# -*- coding: utf-8 -*-
from flask import render_template, current_app, Blueprint

from ..action import (genre_manager, record_manager, scan_manager, export_manager,
                      user_settings)
from ..webapp import basic_auth, db
from ..models import record, scan


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
    img_paths = [img.make_filename() for img in rec.images]

    return render_template('record_view.html', record=rec, FLAGS=record.FLAGS,
                           flag_names=flag_names, img_paths=img_paths)

@bp.route('/imports/')
def import_list():
    scanman = scan_manager.ScanManager(db.session)
    scans = scanman.last_scans()
    return render_template('import_list.html',
                           scans=scans, SCAN_STATUSES=scan.SCAN_STATUSES)


@bp.route('/exports/')
def export_list():
    expman = export_manager.ExportManager(db.session)
    exports = expman.last_exports()
    settings = user_settings.UserSettings(db.session)
    return render_template('export_list.html', exports=exports, settings=settings)
