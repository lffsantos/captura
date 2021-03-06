from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from config.config_file import appconfig

from core.db.model import Base

__author__ = 'lucas'


engine = create_engine(appconfig['database'])


def create_db():
    url_db = appconfig['database']
    create_database(url_db)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def get_engine_db(test=None):
    if test:
        from core.tests.fixtures.helper import get_engine_test
        return get_engine_test()
    return engine

if __name__ == '__main__':
    create_db()