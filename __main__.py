import sys
from jh2.models import Base, Genre, Record, Scan
from jh2.db import engine, Session
from jh2 import scraper


if sys.argv[1] == 'initdb':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    genres = scraper.parse_genres()
    session = Session()
    for g in genres:
        session.add(Genre(title=g['title'], search_term=g['search_term']))
    session.commit()
    session.close()
    print 'Database cleared'
