# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app, render_template

from ..webapp import db
from ..yml import Builder as YMLBuilder

bp = Blueprint('public', __name__)


@bp.route('/yml')
def yml():
    yml_builder = YMLBuilder(session=db.session)
    ctx = {
        'generation_date': yml_builder.generation_date(),
        'genres': yml_builder.genres_list(),
        'offers': yml_builder.offers()
    }
    return render_template('yml.xml', **ctx)


@bp.route('/table')
def table():
    raise NotImplementedError()
