import pika

__author__ = 'lucas'


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
#
# channel.queue_declare(queue='products')
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='products',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()