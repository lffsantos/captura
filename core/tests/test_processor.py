import pytest

from sqlalchemy.orm import Session

from core.db.model import Product
from core.modules.processor import Processor
from core.db.products import Product_db
from core.tests.fixtures.helper import gen_product, insert_products, gen_engine

__author__ = 'lucas'


@pytest.mark.parametrize("test_case", [
    {
        'products': [
            gen_product(
                _id=1,
                url="http://www.epocacosmeticos.com.br/makeup-eraser-"
                    "original-toalha-removedora-de-maquiagem/p",

            )
        ],
        'expected': {
            'title': "MakeUp Eraser Original - Toalha Removedora de Maquiagem"
                      " - Época Cosméticos",
            'name': "MakeUp Eraser Original - Toalha Removedora de Maquiagem"
                     " - Rosa - 1 Unidade",
            'status': 'PROCESSED',
        }
    },
])
def test_Processor_parser_and_update(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    arg = (test_case['products'][0]['id'], test_case['products'][0]['url'])
    Processor._test = True
    Processor.parser_and_update(arg)
    db_session = Session(bind=gen_engine)
    product = db_session.query(Product).get(test_case['products'][0]['id'])
    expected_product = {
        'title': product.title,
        'name': product.name,
        'status': product.status.code
    }
    assert expected_product == test_case['expected']


@pytest.mark.parametrize("test_case", [
    {
        'products': [
            gen_product(
                _id=1,
                url="http://www.epocacosmeticos.com.br/makeup-eraser-"
                    "original-toalha-removedora-de-maquiagem/p",

            ),
            gen_product(
                _id=2,
                url="http://www.epocacosmeticos.com.br/joop-homme-wild-"
                    "eau-de-toilette-joop-perfume-masculino/p",

            ),
            gen_product(
                _id=3,
                url="http://www.epocacosmeticos.com.br/animale-animale-for-"
                    "men-eau-de-toilette-animale-perfume-masculino/p",

            )
        ],
        'msg':[
            [1, "http://www.epocacosmeticos.com.br/makeup-eraser-"
                    "original-toalha-removedora-de-maquiagem/p"],
            [2, "http://www.epocacosmeticos.com.br/joop-homme-wild-"
                    "eau-de-toilette-joop-perfume-masculino/p"],
            [3, "http://www.epocacosmeticos.com.br/animale-animale-for-"
                    "men-eau-de-toilette-animale-perfume-masculino/p"],
        ],
    },
])
def test_Processor_run_processor(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    product_db = Product_db(gen_engine)
    Processor.run_processor(
        test_case['msg'], 1, True
    )
    products = product_db.get_products_for_status('PROCESSED')
    assert len(list(products)) == len(test_case['products'])