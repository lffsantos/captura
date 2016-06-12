import argparse
import json

from datetime import datetime
from pika import BlockingConnection, ConnectionParameters
from products import get_products_for_status, update_status_product

__author__ = 'lucas'


def send_queue_msg(msg, channel, queue):
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(msg))
    print("sent msg")


def calculate_messages(links_per_msg):
    messages = []
    all_messages = []
    for p in get_products_for_status('WAIT'):
        if len(messages) < links_per_msg:
            messages.append((p.id, p.url))
        else:
            all_messages.append(messages)
            messages = []
            messages.append((p.id, p.url))

    all_messages.append(messages)
    return all_messages


class Enqueuer(object):

    @classmethod
    def run_enqueuer(cls, args):

        print("Using QUEUE NAME = " + str(args.queue))

        connection = BlockingConnection(ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=args.queue)

        list_links = calculate_messages(args.links_per_msg)
        if not list_links:
            return 0

        for links in list_links:
            print("Sending msg to %s" % (args.queue))
            if args.queue:
                send_queue_msg(links, channel, args.queue)
                keys = [key for key, l in links]
                update_status_product(keys, 'ENQUEUED')

        connection.close()
        print("Enqueue finished at: %s" % str(datetime.utcnow()))
        return len(list_links)

if __name__ == '__main__':
    """
    TODO
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--links_per_msg", type=int, default=100,
                        help="How many links per message do you want?")
    parser.add_argument("-q", "--queue", help="sqs queue name to connect to")
    args = parser.parse_args()

    if not args.queue:
        raise ValueError("Queue name must not be None")

    Enqueuer.run_enqueuer(args)
