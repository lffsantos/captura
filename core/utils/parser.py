import requests

from bs4 import BeautifulSoup


class Parser(object):

    def __init__(self, url):
        self.session = requests.Session()
        html = self.session.get(url)
        self.content_page = BeautifulSoup(html.content, "html.parser")

    def get_title(self):
        return self.content_page.title.string

    def get_name(self):
        tag = self.content_page.find_all("div", class_="productName")[0]
        return tag.string
