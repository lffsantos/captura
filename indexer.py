import csv
from file_util import create_file
from products import get_products_for_status, update_status_product

__author__ = 'lucas'


def export_data_to_csv(file_name, products):
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

    update_status_product(keys, 'INDEXED')

if __name__ == '__main__':
    products = get_products_for_status('PROCESSED')
    export_data_to_csv('products.csv', products)