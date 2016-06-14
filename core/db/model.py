from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType

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