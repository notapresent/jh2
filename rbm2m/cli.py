# -*- coding: utf-8 -*-
import click

from redis import StrictRedis

from rbm2m.models.base import Base
from rbm2m.models import *
from rbm2m.models.genremanager import GenreManager
from helpers import make_session, make_config, make_engine


config = make_config()
engine = make_engine(config)



@click.group()
def main():
    pass


@main.command()
def createdb():
    Base.metadata.create_all(bind=engine)
    click.echo('Database initialized')


@main.command()
def dropdb():
    Base.metadata.drop_all(bind=engine)
    click.echo('Database dropped')


@main.command()
def import_genres():
    session = make_session(engine)
    GenreManager.import_genres(session)
    click.echo('Genres imported')


@main.command()
def flush_redis():
    redis = StrictRedis.from_url(config.REDIS_URL)
    redis.flushdb()
    click.echo('Redis DB flushed')
