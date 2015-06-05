# -*- coding: utf-8 -*-
import click
from redis import StrictRedis

from rbm2m.models.base import Base
from .models import Genre
from rbm2m.action import scraper
from .action import user_settings, genre_manager
from helpers import make_session, make_config, make_engine

config = make_config()
engine = make_engine(config)


@click.group()
def main():
    """
        Command grouping
    """
    pass


@main.command()
def createdb():
    """
        Create database tables
    """
    Base.metadata.create_all(bind=engine)
    click.echo('Database initialized')


@main.command()
def dropdb():
    """
        Drop database tables
    """
    Base.metadata.drop_all(bind=engine)
    click.echo('Database dropped')


@main.command()
def import_genres():
    """
        Import genres from rbm and save in DB
    """
    session = make_session(engine)
    genman = genre_manager.GenreManager(session)
    genman.import_genres()
    session.commit()
    click.echo('Genres imported')


@main.command()
def flush_redis():
    """
        Flush redis db
    """
    redis = StrictRedis.from_url(config.REDIS_URL)
    redis.flushdb()
    click.echo('Redis DB flushed')


@main.command()
def reset_settings():
    """
        Reset user settings to default values
    """
    session = make_session(engine)
    settings = user_settings.UserSettings(session)
    settings.reset()
    session.commit()
    click.echo('User settings reset to default values')
