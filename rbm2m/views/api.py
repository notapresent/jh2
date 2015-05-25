# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from rbm2m import basic_auth, db
from rbm2m.models import scheduler
from rbm2m.models.db import get_stats, Scan


bp = Blueprint('api', __name__)


@bp.before_request
def check_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


@bp.route('/stats')
def status():
    stats = get_stats(db.session)
    scans = Scan.get_last_scans()
    return jsonify({'stats': stats, 'scans': scans})


@bp.route('/run_scan/<int:genre_id>')
def run_scan(genre_id):
    try:
        scan = scheduler.start_scan(genre_id, db.session)
    except scheduler.AlreadyStarted as e:
        return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': True, 'scan_id': scan.id})


@bp.route('/abort_scan/<int:scan_id>')
def abort_scan(scan_id):
    try:
        scheduler.abort_scan(scan_id)
    except scheduler.ScheduleError as e:
        return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': True})
