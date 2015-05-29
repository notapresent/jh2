# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app, request

from ..webapp import db, redis, basic_auth
from ..models import Genre
from rbm2m import scheduler
from ..action import stats

bp = Blueprint('api', __name__)


@bp.before_request
def check_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


@bp.route('/stats')
def get_stats():
    overview = stats.get_overview(db.session)
    scans = stats.active_scans(db.session)
    return jsonify({'stats': overview, 'scans': scans})


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

@bp.route('/update_genre')
def update_genre():
    genre_id = request.args['gid']
    field = request.args['f']
    value = int(request.args['v'])

    db.session.query(Genre) \
        .filter_by(id=genre_id) \
        .update({getattr(Genre, field): value})
    db.session.commit()
    return jsonify({'success': True})
