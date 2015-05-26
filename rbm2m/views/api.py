# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app

from ..webapp import db, redis, basic_auth
from ..models import Scan, scheduler
from ..helpers import get_stats


bp = Blueprint('api', __name__)


@bp.before_request
def check_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


@bp.route('/stats')
def status():
    stats = get_stats(db.session)
    scans = db.session.query(Scan).order_by(-Scan.started_at).limit(5).all()
    return jsonify({'stats': stats, 'scans': scans})


@bp.route('/run_scan/<int:genre_id>')
def run_scan(genre_id):
    sched = scheduler.Scheduler(db.session, redis._redis_client,
                                current_app.config['RQ_QUEUE_NAME'])
    try:
        sched.run_scan(genre_id)
    except scheduler.AlreadyStarted as e:
        return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': True})


@bp.route('/abort_scan/<int:scan_id>')
def abort_scan(scan_id):
    sched = scheduler.Scheduler(db.session, redis._redis_client,
                                current_app.config['RQ_QUEUE_NAME'])
    try:
        sched.abort_scan(scan_id)
    except scheduler.SchedulerError as e:
        return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': True})
