import pytest
from config.database import create_db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database


@pytest.yield_fixture
def session_db():
    url_db = 'postgresql://postgres:123@localhost:5432/desafio_test'

    create_db('desafio_test')
    engine = create_engine(url_db)

    yield Session(bind=engine)

    drop_database(url_db)