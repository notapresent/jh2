# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app, request

from ..webapp import db, redis, basic_auth
from ..action import stats, scanner, record_manager, genre_manager

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
@bp.route('/abort_scan/', defaults={'scan_id': None})
def abort_scan(scan_id=None):
    scn = scanner.Scanner(current_app.config, db.session, redis)

    if scan_id is None:
        scan_id = int(request.args.get('scan_id'))

    try:
        scn.abort_scan(scan_id)
    except scanner.ScanError as e:  # no such scan or scan not started
        return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': True})


@bp.route('/update_genre')
def update_genre():
    genre_id = int(request.args['gid'])
    field = request.args['f']
    value = int(request.args['v'])
    genman = genre_manager.GenreManager(db.session)
    genre = genman.get(genre_id)
    setattr(genre, field, value)
    return jsonify({'success': True})


@bp.route('/record_list')
def record_list():
    filters = {k[2:]: int(v) for k, v in request.args.items() if k.startswith('f_') and v}
    search_term = request.args.get('search', None)
    order = request.args.get('order', 'id')
    offset = request.args.get('offset', 0)

    recman = record_manager.RecordManager(db.session)
    records = recman.list(filters=filters, search=search_term, order=order,
                          offset=offset)
    return jsonify({'records': [rec.to_dict() for rec in records]})

@bp.route('/record/<int:rec_id>/toggle_flag')
def toggle_record_flag(rec_id):
    flagname = request.args.get('flagname')
    recman = record_manager.RecordManager(db.session)
    return jsonify({'success': recman.toggle_flag(rec_id, flagname)})


