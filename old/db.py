from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jh2.config import MYSQL_URL


engine = create_engine(MYSQL_URL)
Session = sessionmaker(bind=engine)
