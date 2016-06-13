from parser import Parser
import pytest
__author__ = 'lucas'


@pytest.mark.parametrize("test_case", [
    {
        'url': "http://www.epocacosmeticos.com.br/makeup-eraser-"
                    "original-toalha-removedora-de-maquiagem/p",
        'expected': {
            'title': "MakeUp Eraser Original - Toalha Removedora de Maquiagem"
                      " - Época Cosméticos",
            'name': "MakeUp Eraser Original - Toalha Removedora de Maquiagem"
                     " - Rosa - 1 Unidade",
        }
    },
])
def test_parser(test_case):
    parser = Parser(test_case['url'])
    expected = {
        'title': parser.get_title(),
        'name': parser.get_name(),
    }
    assert expected == test_case['expected']
