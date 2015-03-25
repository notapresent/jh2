import datetime
import math

from rq import Queue
from redis import Redis

from jh2.models import Genre, Record, Scan
from jh2.db import Session
from jh2.scraper import scrape_page, ScrapeFailed, count_records


redis_conn = Redis()
q = Queue(connection=redis_conn)


def start_scan(genre_id):
    session = Session()
    genre = session.query(Genre).get(genre_id)
    num_records = count_records(genre.search_term)

    scan = Scan(
        start_date=datetime.datetime.utcnow(),
        genre_id=genre_id,
        num_records=num_records,
        status='In progress'
    )
    session.add(scan)
    session.commit()

    for i in xrange(1, 1 + int(math.ceil(num_records / 25.0))):
        job = q.enqueue(scan_page, args=(scan.id, i))


def end_scan(scan_id, status):
    session = Session()
    scan = session.query(Scan).get(scan_id)
    scan.status = status
    scan.end_date = datetime.datetime.utcnow()
    session.commit()


def scan_page(scan_id, page_no):
    session = Session()
    scan = session.query(Scan).get(scan_id)
    try:
        items = scrape_page(scan.genre.search_term, page_no)
    except ScrapeFailed as err:
        end_scan(scan_id, str(err))

    if not items:
        end_scan(scan_id, 'Success')
        return


    ge = session.query(Genre).filter(Genre.title == u'Rock & Pop').first()
    for i in items:
        # ge = session.query(Genre).filter(Genre.title == i['genre']).first()

        # if not ge:
        #     ge = Genre(title=i['genre'])
        #     session.add(ge)

        rec = Record(
            id = i['oid'],
            import_date=datetime.datetime.now(),
            artist=i['artist'],
            title=i['title'],
            label=i['label'],
            notes=i['notes'],
            grade=i['grade'],
            price=i['price'],
            img_url=i['thumbnail'],
            genre=ge
        )
        session.add(rec)

    session.commit()
    # job = q.enqueue(scan_page, args=(scan_id, page_no+1))

