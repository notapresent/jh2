# -*- coding: utf-8 -*-
import click

from rbm2m import db, create_app, config
from rbm2m.models.genremanager import GenreManager

@click.group()
def main():
    pass


@main.command()
def initdb():
    app = create_app(config.app_environment)
    with app.app_context():
        db.create_all()
        GenreManager.import_genres(db.session)
    click.echo('Initialized the database')


@main.command()
def dropdb():
    app = create_app(config.app_environment)
    with app.app_context():
        db.drop_all()
    click.echo('Dropped the database')
