from db.model import Base, Product
from pika import BlockingConnection, ConnectionParameters
import random as rand
from string import ascii_letters
from random import choice
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import drop_database, create_database

url_db = 'postgresql://postgres:123@localhost:5432/desafio_test'


def create_db_test():
    create_database(url_db)
    session = sessionmaker()
    engine = create_engine(url_db)
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    return engine


@pytest.yield_fixture
def gen_engine():

    _engine = create_db_test()

    yield _engine

    drop_database(url_db)


def get_engine_test():
    return create_engine(url_db)


def random_string(size=10):
    return ''.join(choice(ascii_letters) for _ in range(size))


def rand_int():
    return rand.random()


def gen_product(_id=None, url=None, title=None, name=None, status='WAIT'):
    product = {
        'id': _id if _id else rand_int(),
        'url': url if url else random_string(12),
    }
    if title:
        product['title'] = title
    if name:
        product['name'] = name
    if status:
        product['status'] = status

    return product


def insert_products(products, engine):
    session_db = Session(bind=engine)
    for product in products:
        p = Product(**product)
        session_db.add(p)
        session_db.commit()


def connection_queue(queue='test'):
    connection = BlockingConnection(ConnectionParameters(host='localhost'))
    return connection


def close_conn_queue(connection, queue='test'):
    channel = connection.channel()
    channel.queue_delete(queue)
    connection.close()