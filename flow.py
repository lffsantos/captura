import argparse

from core.modules.crawler import Crawler
from core.modules.enqueuer import Enqueuer


__author__ = 'lucas'

if __name__ == '__main__':
    """
    O flow realiza a operação de crawler e de enqueuer
    e.g: ./flow.py -l 7 -q 'products'
    """
    urls = ['http://www.epocacosmeticos.com.br']
    crawler = Crawler(urls)
    crawler.run()
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--links_per_msg", type=int, default=10,
                        help="How many links per message do you want?")
    parser.add_argument("-q", "--queue", help="sqs queue name to connect to")
    parser.add_argument("-t", "--test", type=bool, default=False,
                        help="sqs queue name to connect to")
    args = parser.parse_args()
    Enqueuer.run_enqueuer(args)
