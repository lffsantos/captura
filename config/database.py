from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__author__ = 'lucas'

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String,  nullable=True)
    name = Column(String,  nullable=True)


# engine = create_engine('sqlite:///database.sqlite')
engine = create_engine('postgresql://postgres:123@localhost:5432/desafio')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def get_engine_db():
    return engine