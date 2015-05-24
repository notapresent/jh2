# -*- coding: utf-8 -*-
import json

from flask import render_template, abort, url_for, Blueprint

from rbm2m import basic_auth


bp = Blueprint('api', __name__)


@bp.route('/status')
@basic_auth.required
def status():
    return json.dumps({'status': 'TODO'})
