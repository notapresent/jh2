# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, render_template, request

from ..webapp import db
from ..action import export_manager, genre_manager, export


bp = Blueprint('public', __name__)
logger = logging.getLogger(__name__)


@bp.route('/yml')
def yml():
    """
        YML export endpoint
    """
    genman = genre_manager.GenreManager(db.session)
    exporter = export.Exporter(session=db.session)
    ctx = {
        'generation_date': exporter.generation_date(),
        'genres': genman.exported_list(),
        'offers': exporter.offers()
    }

    exp = log_export('yml', request.remote_addr, request.user_agent)
    message = "{} export #{} for {}@{} completed"
    logger.info(message.format(exp.format, exp.id, exp.user_agent, exp.ip))

    return render_template('yml.xml', **ctx)


@bp.route('/table')
def table():
    """
        HTML table export endpoint
    """
    exporter = export.Exporter(session=db.session)
    ctx = {
        'generation_date': exporter.generation_date(),
        'rows': exporter.tabrows()
    }

    exp = log_export('table', request.remote_addr, request.user_agent)
    message = "{} export #{} for {}@{} completed"
    logger.info(message.format(exp.format, exp.id, exp.user_agent, exp.ip))

    return render_template('table.html', **ctx)


def log_export(fmt, ip, user_agent):
    """
        Save export entry and return it
    """
    expman = export_manager.ExportManager(db.session)
    expdata = {
        'user_agent': user_agent,
        'ip': ip,
        'format': fmt
    }
    return expman.from_dict(expdata)
