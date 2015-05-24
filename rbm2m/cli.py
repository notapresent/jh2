# -*- coding: utf-8 -*-
import os

import click

from rbm2m import create_app
from rbm2m.models.db import *
from rbm2m.models.genremanager import GenreManager

app_env = os.environ.get('RBM2M_ENV', 'Production')


@click.group()
def main():
    pass


@main.command()
def initdb():
    app = create_app(app_env)
    with app.app_context():
        db.drop_all()
        db.create_all()
        GenreManager.import_genres(db.session)
    click.echo('Initialized the database')


@main.command()
def dropdb():
    app = create_app(app_env)
    with app.app_context():
        db.drop_all()
    click.echo('Dropped the database')
