from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, ChoiceType

__author__ = 'lucas'

Base = declarative_base()


STATUS_CHOICES = (
    ('WAIT', 'wait'),
    ('ENQUEUED', 'Enqueued'),
    ('PROCESSED', 'Processed'),
    ('INDEXED', 'Indexed'),
)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String,  nullable=True)
    name = Column(String,  nullable=True)
    status = Column(ChoiceType(STATUS_CHOICES, impl=String()), default='WAIT')


# engine = create_engine('sqlite:///database.sqlite')
# engine = create_engine('postgresql://postgres:123@localhost:5432/desafio')


engine = create_engine('postgresql://postgres:123@localhost:5432/captura')


def create_db(database):
    url_db = 'postgresql://postgres:123@localhost:5432/'+database
    create_database(url_db)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def get_engine_db(test=None):
    if test:
        from tests.helper import get_engine_test
        return get_engine_test()
    return engine

if __name__ == '__main__':
    create_db('captura')