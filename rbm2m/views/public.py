# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, render_template, request

from ..webapp import db
from ..yml import Builder as YMLBuilder
from ..action import export_manager

bp = Blueprint('public', __name__)
logger = logging.getLogger(__name__)


@bp.route('/yml')
def yml():
    yml_builder = YMLBuilder(session=db.session)
    ctx = {
        'generation_date': yml_builder.generation_date(),
        'genres': yml_builder.genres_list(),
        'offers': yml_builder.offers()
    }
    expman = export_manager.ExportManager(db.session)
    expdata = {
        'user_agent': request.environ.get('HTTP_USER_AGENT'),
        'ip': request.environ.get('REMOTE_ADDR'),
        'format': 'yml'
    }
    exp = expman.from_dict(expdata)
    message = "YML export for {}@{} completed"
    logger.info(message.format(request.environ.get('HTTP_USER_AGENT'),
                               request.environ.get('REMOTE_ADDR')))
    return render_template('yml.xml', **ctx)


@bp.route('/table')
def table():
    message = "Table export for {}@{} completed"
    logger.info(message.format(request.environ.get('HTTP_USER_AGENT'),
                               request.environ.get('REMOTE_ADDR')))
    raise NotImplementedError('Not yet')
