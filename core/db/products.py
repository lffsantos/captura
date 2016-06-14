from sqlalchemy.orm import Session

from core.db.model import Product

__author__ = 'lucas'


class Product_db(object):

    __instance = None
    _db = None

    def __init__(self, engine):
        self._db = Session(bind=engine)

    def get_products_for_status(self, status):
        return self._db.query(Product).filter_by(status=status)

    def update_status_products(self, keys, status):
        products = self._db.query(Product).filter(Product.id.in_(keys))
        for p in products:
            p.status = status
            self._db.add(p)

        self._db.commit()

    def update_product(self, key, title, name, status):
        product = self._db.query(Product).get(key)
        product.title = title
        product.name = name
        product.status = status
        self._db.add(product)
        self._db.commit()


# if __name__ == '__main__':
#     products = get_products_for_status('WAIT')
#     print(len(list(products)))
#     update_status_products([276, 277], 'WAIT')
