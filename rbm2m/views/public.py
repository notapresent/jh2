# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app, render_template

from ..webapp import db
from ..yml import Builder as YMLBuilder

bp = Blueprint('public', __name__)


@bp.route('/yml')
def yml():
    yml_builder = YMLBuilder(session=db.session)
    return render_template('yml.xml', **yml_builder.build())


@bp.route('/table')
def table():
    raise NotImplementedError()

