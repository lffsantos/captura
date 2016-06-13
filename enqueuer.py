import argparse
import json

from datetime import datetime
from database import get_engine_db
from pika import BlockingConnection, ConnectionParameters
from products import Product_db

__author__ = 'lucas'


def send_queue_msg(msg, channel, queue):
    """
    Recebe a mensagem com os links e envia para uma fila
    """
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(msg))
    print("sent msg")


def calculate_messages(product_db, links_per_msg):
    """
    Consulta no banco de dados os links com status 'WAIT', para calcular
    a quantidade de links por mensagens.

    :return list of list de links
    """
    messages = []
    all_messages = []
    for p in product_db.get_products_for_status('WAIT'):
        if len(messages) < links_per_msg:
            messages.append((p.id, p.url))
        else:
            all_messages.append(messages)
            messages = []
            messages.append((p.id, p.url))

    all_messages.append(messages)
    return all_messages


class Enqueuer(object):
    """
    Classe que vai enfileirar as mensagens
    """
    @classmethod
    def run_enqueuer(cls, args):
        product_db = Product_db(get_engine_db(args.test))

        print("Using QUEUE NAME = " + str(args.queue))

        connection = BlockingConnection(ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=args.queue)

        list_links = calculate_messages(product_db, args.links_per_msg)
        if not list_links[0]:
            return 0

        for links in list_links:
            print("Sending msg to %s" % (args.queue))
            if args.queue:
                send_queue_msg(links, channel, args.queue)
                keys = [key for key, l in links]
                product_db.update_status_products(keys, 'ENQUEUED')

        connection.close()
        print("Enqueue finished at: %s" % str(datetime.utcnow()))
        return len(list_links)

if __name__ == '__main__':
    """
    Programa responsável por enfileirar os links que ainda não tem todas as
    informações.
    e.g: ./enqueuer.py -l 7 -q queue
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--links_per_msg", type=int, default=10,
                        help="How many links per message do you want?")
    parser.add_argument("-q", "--queue", help="sqs queue name to connect to")
    parser.add_argument("-t", "--test", type=bool, default=False,
                        help="sqs queue name to connect to")
    args = parser.parse_args()

    if not args.queue:
        raise ValueError("Queue name must not be None")

    Enqueuer.run_enqueuer(args)
