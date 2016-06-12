import argparse
from crawler import Crawler
from enqueuer import Enqueuer

__author__ = 'lucas'

if __name__ == '__main__':
    urls = ['http://www.epocacosmeticos.com.br']
    crawler = Crawler(urls)
    crawler.run()
    parser = argparse.ArgumentParser(prefix_chars='-+')
    parser.add_argument('+links_per_msg')
    parser.add_argument('++queue')
    args = parser.parse_args('+links_per_msg 100 ++queue products'.split())
    Enqueuer.run_enqueuer(args)
