# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort


webui = Blueprint('webui', __name__, template_folder='templates')


@webui.route('/')
def show():
    return render_template('dashboard.html')
