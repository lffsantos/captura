import argparse
import concurrent.futures
import json
from database import get_engine_db
from parser import Parser
from pika import BlockingConnection, ConnectionParameters
from products import Product_db

__author__ = 'lucas'


class Processor(object):
    _test = False

    @classmethod
    def parser_and_update(cls, args):
        key, url = args
        content = Parser(url)
        Product_db(get_engine_db(cls._test)).update_product(
            key, content.get_title(), content.get_name(), 'PROCESSED'
        )

    @classmethod
    def run_processor(cls, body, workers, test=False):
        cls._test = test
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            for arg, _ in zip(body, executor.map(cls.parser_and_update, body)):
                print(" %r updated" % arg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", type=int, default=4,
                        help="number of workers for parallel processing")
    parser.add_argument("-q", "--queue", help="queue name to connect to")
    parser.add_argument("-t", "--test", type=bool, default=False,
                        help="sqs queue name to connect to")
    args = parser.parse_args()

    if not args.queue:
        raise ValueError("Queue name must not be None")

    connection = BlockingConnection(ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body.decode('utf-8')))
        Processor.run_processor(
            json.loads(body.decode('utf-8')), args.workers, args.test
        )
        print(" [x] Done")

    channel.basic_consume(callback, queue=args.queue, no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
