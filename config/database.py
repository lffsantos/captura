from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database

__author__ = 'lucas'

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String,  nullable=True)
    name = Column(String,  nullable=True)


# engine = create_engine('sqlite:///database.sqlite')
# engine = create_engine('postgresql://postgres:123@localhost:5432/desafio')


def create_db(database):
    url_db = 'postgresql://postgres:123@localhost:5432/'+database
    create_database(url_db)
    engine = create_engine(url_db)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def get_engine_db():
    return create_engine('postgresql://postgres:123@localhost:5432/desafiox')

if __name__ == '__main__':
    create_db('desafiox')