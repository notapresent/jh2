# -*- coding: utf-8 -*-
import logging

from flask import (Blueprint, render_template, request, send_from_directory,
                   current_app, Response, stream_with_context)

from ..webapp import db
from ..action import exporter


bp = Blueprint('public', __name__)
logger = logging.getLogger(__name__)


@bp.route('/yml')
def yml():
    """
        YML export endpoint
    """

    exp = exporter.YMLExporter(db.session, filters={'format':'LP'})
    exp.log_export(client_ip(), request.user_agent)
    ctx = {
        'generation_date': exp.generation_date(),
        'genres': exp.category_list(),
        'offers': exp.offers()
    }
    return Response(stream_with_context(stream_template('yml.xml', **ctx)))


@bp.route('/table')
def table():
    """
        Table export endpoint
    """
    exp = exporter.TableExporter(db.session)
    exp.log_export(client_ip(), request.user_agent)

    ctx = {
        'genres': exp.category_list(),
        'rows': exp.rows()
    }
    return Response(stream_with_context(stream_template('table.html', **ctx)))


@bp.route('/media/<path:path>')
def serve_media(path):
    return send_from_directory(current_app.config['MEDIA_DIR'], path)


def client_ip():
    """
        Returns client ip address
    """
    if 'HTTP_X_REAL_IP' in request.environ:
        return request.environ['HTTP_X_REAL_IP']

    return request.remote_addr


def stream_template(template_name, **context):
    """
        Stream rendered template output
    """
    current_app.update_template_context(context)
    t = current_app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv
