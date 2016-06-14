import pytest

from sqlalchemy.orm import Session

from core.db.model import Product
from core.db.products import Product_db
from core.tests.fixtures.helper import gen_product, insert_products, gen_engine



__author__ = 'lucas'


@pytest.mark.parametrize("test_case", [
    {
        'products':
            [gen_product(_id=i, status='WAIT') for i in range(1, 11)] +
            [gen_product(_id=i, status='ENQUEUED') for i in range(11, 15)],
        'status': 'WAIT',
        'expected_products': 10
    },
    {
        'products':
            [gen_product(_id=i, status='WAIT') for i in range(1, 6)] +
            [gen_product(_id=i, status='ENQUEUED') for i in range(6, 10)],
        'status': 'ENQUEUED',
        'expected_products': 4
    },
])
def test_get_products_for_status(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    product_db = Product_db(gen_engine)
    products = product_db.get_products_for_status(test_case['status'])
    assert len(list(products)) == test_case['expected_products']


@pytest.mark.parametrize("test_case", [
    {
        'keys': [1, 2],
        'products': [gen_product(_id=i, status='WAIT') for i in range(1, 6)],
        'status': 'ENQUEUED',
        'expected_update': 2
    },
    {
        'keys': [1, 2, 3],
        'products': [gen_product(_id=i, status='WAIT') for i in range(1, 5)],
        'status': 'ENQUEUED',
        'expected_update': 3
    },
])
def test_update_status_product(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    product_db = Product_db(gen_engine)
    product_db.update_status_products(test_case['keys'], test_case['status'])
    products = product_db.get_products_for_status(test_case['status'])
    assert len(list(products)) == test_case['expected_update']


@pytest.mark.parametrize("test_case", [
    {
        'products': [gen_product(_id=1, status='WAIT')],
        'params': {
            'key': 1,
            'title': 'title1',
            'name': 'name1',
            'status': 'ENQUEUED',
        },
    },
    {
        'products': [gen_product(_id=2, status='WAIT')],
        'params': {
            'key': 2,
            'title': 'title2',
            'name': 'name2',
            'status': 'PROCESSED',
        },
    },
])
def test_update_product(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    product_db = Product_db(gen_engine)
    product_db.update_product(**test_case['params'])
    db_session = Session(bind=gen_engine)
    product = db_session.query(Product).get(test_case['params']['key'])
    expected_product = {
        'key': product.id,
        'title': product.title,
        'name': product.name,
        'status': product.status.code
    }
    assert expected_product == test_case['params']
