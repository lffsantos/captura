import argparse
import pytest

from products import Product_db
from enqueuer import send_queue_msg, calculate_messages, Enqueuer
from tests.helper import (
    connection_queue, close_conn_queue, gen_product, gen_engine,
    insert_products
)

__author__ = 'lucas'


@pytest.mark.parametrize("msg", [
    ("hello word"),
    (["hello", "word"]),
    (1),
])
def test_send_queue_msg(msg):
    queue = 'test'
    conn = connection_queue(queue)
    channel = conn.channel()
    channel.queue_declare(queue=queue)
    send_queue_msg(msg, channel, 'test')
    channel = channel.queue_declare(queue=queue)
    q_len = channel.method.message_count
    assert q_len == 1
    close_conn_queue(conn, queue='test')


@pytest.mark.parametrize("test_case", [
    {
        'products': [
            gen_product(_id=i, status='WAIT') for i in range(1, 101)
        ],
        'links_per_msg': 10,
        'expected_msgs': 10
    },
    {
        'products': [
            gen_product(_id=i, status='WAIT') for i in range(1, 70)
        ],
        'links_per_msg': 5,
        'expected_msgs': 14
    },
])
def test_calculate_messages(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    product_db = Product_db(gen_engine)
    msgs = calculate_messages(product_db, test_case['links_per_msg'])
    assert len(msgs) == test_case['expected_msgs']



@pytest.mark.parametrize("test_case", [
    {
        'products': [
            gen_product(_id=i, status='WAIT') for i in range(1, 101)
        ],
        'queue_name': 'test',
        'links_per_msg': 10,
        'expected_msgs': 10
    },
    {
        'products': [
            gen_product(_id=i, status='WAIT') for i in range(1, 71)
        ],
        'queue_name': 'test',
        'links_per_msg': 5,
        'expected_msgs': 14
    },
])
def test_Enqueuer_run_enqueuer(test_case, gen_engine):
    insert_products(test_case['products'], gen_engine)
    parser = argparse.ArgumentParser(prefix_chars='-+')
    parser.add_argument('+links_per_msg', type=int)
    parser.add_argument('++queue')
    parser.add_argument('+++test', type=bool)
    l = str(test_case['links_per_msg'])
    queue = test_case['queue_name']
    args = parser.parse_args(
        ("+links_per_msg "+l+" ++queue "+queue+" +++test true").split()
    )
    Enqueuer.run_enqueuer(args)
    conn = connection_queue(test_case['queue_name'])
    channel = conn.channel()
    channel = channel.queue_declare(queue=test_case['queue_name'])
    q_len = channel.method.message_count
    assert q_len == test_case['expected_msgs']
    close_conn_queue(conn, queue=test_case['queue_name'])




