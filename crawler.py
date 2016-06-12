import re
import requests
import concurrent.futures

from config.database import Product, get_engine_db
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

__author__ = 'lucas'


class Crawler(object):

    def __init__(self, urls, workers=3):
        self.urls = urls
        self.workers = workers
        self.session = requests.Session()

    def conn_url(self, url):
        return self.session.get(url)

    @staticmethod
    def get_content(page):
        return BeautifulSoup(page, "html.parser")

    @staticmethod
    def get_links(page):
        return page.find_all('a', href=re.compile(r'/p$'))

    @staticmethod
    def save_on_db(links, db):
        for link in links:
            url = link.get('href')
            product = db.query(Product).filter_by(url=url)
            if len(list(product)) == 1:
                # this product already exists on database
                continue

            product = Product(url=link.get('href'))
            db.add(product)
            db.commit()

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            db = Session(bind=get_engine_db())
            future_to_url = {executor.submit(self.conn_url, url): url for url in self.urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    page = future.result()
                    links = self.get_links(self.get_content(page.content))
                    self.save_on_db(links, db)
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))


if __name__ == '__main__':
    urls = ['http://www.epocacosmeticos.com.br']
    crawler = Crawler(urls)
    # start = time.time()
    crawler.run()
    # end = time.time()
    # print(end-start)
