from config.database import  Product
import random
import pytest
from crawler import Crawler
from .helper import session_db

__author__ = 'lucas'


def gen_links(n, repeat=0, n_other_links=2):
    product_links = [
        '<a href="http://'+str(random.random())+'/lacie/p">tile</a>'
        for _ in range(n)
    ]

    if repeat:
       product_links = product_links[:n-repeat] + product_links[:repeat]

    other_links = ['<a href="http://'+str(random.random())+'/blabla/">tile</a>'
                   for _ in range(n_other_links)]

    return product_links + other_links


def gen_html_doc(links=None, title="Default"):
    links = links or gen_links(2)
    html_doc = "<title>"+title+"</title>"
    html_doc += "<p class=\"story\">htmldsadsadsdas</p>"
    html_doc += "".join(links)
    html_doc += "<p class=\"story\">.babbabbababbaba</p>"
    return html_doc


@pytest.mark.parametrize("html, expected", [
    (gen_html_doc(title="Title1"), "Title1"),
    (gen_html_doc(title="Title2"), "Title2"),
    (gen_html_doc(title="Title3"), "Title3")
])
def test_get_page_content(html, expected):
    page_content = Crawler.get_content(html)
    assert page_content.title.string == expected


@pytest.mark.parametrize("html, expected", [
    (gen_html_doc(gen_links(2)), 2),
    (gen_html_doc(gen_links(4)), 4),
    (gen_html_doc(gen_links(10)), 10),
])
def test_get_links(html, expected):
    page_content = Crawler.get_content(html)
    links = Crawler.get_links(page_content)
    assert len(links) == expected


@pytest.mark.parametrize("html, expected", [
    (gen_html_doc(gen_links(2)), 2),
    (gen_html_doc(gen_links(4, 1)), 3),
    (gen_html_doc(gen_links(5, 3)), 3),
])
def test_save_on_db(html, expected, session_db):
    page_content = Crawler.get_content(html)
    links = Crawler.get_links(page_content)
    Crawler.save_on_db(links, session_db)
    products = session_db.query(Product).all()
    assert len(list(products)) == expected