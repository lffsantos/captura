from copy import copy
from config.database import get_engine_db, Product
from sqlalchemy.orm import Session

__author__ = 'lucas'


def get_products_for_status(status):
    db = Session(bind=get_engine_db())
    return db.query(Product).filter_by(status=status)


def update_status_product(keys, status):
    db = Session(bind=get_engine_db())
    products = db.query(Product).filter(Product.id.in_(keys))
    for p in products:
        p.status = status
        db.add(p)

    db.commit()


def update_product(key, title, name, status):
    db = Session(bind=get_engine_db())
    product = db.query(Product).get(key)
    product.title = title
    product.name = name
    product.status = status
    db.add(product)
    db.commit()


# if __name__ == '__main__':
#     products = get_products_for_status('WAIT')
#     print(len(list(products)))
#     update_status_product([276, 277], 'WAIT')
