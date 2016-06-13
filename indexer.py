import csv
from config_file import appconfig
from database import get_engine_db
from file_util import create_file
from products import Product_db

__author__ = 'lucas'


class Indexer(object):
    _test = False

    @classmethod
    def export_data_to_csv(cls, file_name, products):
        """
        Export list of products from database to file_name.csv
        :param file_name: name of file
        :param products: list of products
        """
        header = ['nome_do_produto', 'título', 'url']
        create_file(file_name, header)
        keys = []
        with open(file_name, 'a') as csvfile:
            for product in products:
                spam = csv.writer(csvfile, delimiter=',')
                spam.writerow([product.name, product.title, product.url])
                keys.append(product.id)

        Product_db(get_engine_db(cls._test)).update_status_products(keys, 'INDEXED')

if __name__ == '__main__':
    """
    Responsável por gerar o arquivo 'file.csv', pesquisa no banco de dados
    os produtos que foram processados e gera um arquivo com os dados
    desse produto.
    e.g: python indexer.py
    """
    product_db = Product_db(get_engine_db())
    products = product_db.get_products_for_status('PROCESSED')
    Indexer.export_data_to_csv(appconfig['local_file_name'], products)