# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app, request

from ..webapp import db, redis, basic_auth
from ..models import Genre
from ..action import stats, scanner

bp = Blueprint('api', __name__)


def jsonified_route():
    pass


def route(self, rule, **options):
    """Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
    :func:`url_for` function is prefixed with the name of the blueprint.
    """
    def decorator(f):
        endpoint = options.pop("endpoint", f.__name__)
        self.add_url_rule(rule, endpoint, f, **options)
        return f
    return decorator


@bp.before_request
def check_auth():
    if not basic_auth.authenticate():
        return basic_auth.challenge()


# TODO auto-jsonify all responses from this blueprint
# see https://github.com/mattupstate/overholt/blob/master/overholt/api/__init__.py#L36-L51

@bp.route('/stats')
def get_stats():
    overview = stats.get_overview(db.session)
    scans = stats.active_scans(db.session)
    return jsonify({'stats': overview, 'scans': scans})


@bp.route('/run_scan/<int:genre_id>')
@bp.route('/run_scan/', defaults={'genre_id': None})
def run_scan(genre_id):
    sc = scanner.Scanner(current_app.config, db.session, redis._redis_client)
    try:
        sc.enqueue_scan(genre_id)
    except scanner.ScanError as e:      # Scan already queued
        return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': True})


@bp.route('/abort_scan/<int:scan_id>')
def abort_scan(scan_id=None):
    scn = scanner.Scanner(current_app.config, db.session, redis)
    try:
        scn.abort_scan(scan_id)
    except scanner.ScanError as e:  # no such scan or scan not started
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
