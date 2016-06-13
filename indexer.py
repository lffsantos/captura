import csv
from config.database import get_engine_db
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
    product_db = Product_db(get_engine_db())
    products = product_db.get_products_for_status('PROCESSED')
    Indexer.export_data_to_csv('products.csv', products)