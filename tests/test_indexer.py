import os
from indexer import Indexer
from products import Product_db
import pytest
from tests.helper import gen_product, gen_engine, insert_products

__author__ = 'lucas'


@pytest.mark.parametrize("test_case", [
    {
        'products': [
            gen_product(
                _id=1,
                url="url1",
                status='PROCESSED',
                title='title1',
                name='name1',

            ),
            gen_product(
                _id=2,
                url="url2",
                status='PROCESSED',
                title='title2',
                name='name2',

            ),
            gen_product(
                _id=3,
                url="url3",
                status='PROCESSED',
                title='title3',
                name='name3',

            )
        ],
        'expected': [
            'nome_do_produto,título,url\n'
            'name1,title1,url1\n'
            'name2,title2,url2\n'
            'name3,title3,url3\n'
        ]
    },
])
def test_export_data_to_csv(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    product_db = Product_db(gen_engine)
    products = product_db.get_products_for_status('PROCESSED')
    Indexer._test = True
    Indexer.export_data_to_csv('test.csv', products)
    with open('test.csv', 'r') as csvfile:
        result = csvfile.read()

    assert result == test_case['expected'][0]
    os.remove('test.csv')
