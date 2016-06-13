import pika

__author__ = 'lucas'


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

response = channel.queue_declare(queue='products11')

# channel.queue_delete(queue='products11111')
channel.basic_publish(exchange='',
                      routing_key='products11',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
response1 = channel.queue_declare('products11', passive=True)
print('The queue has {0} messages'.format(response.message_count))
connection.close()


# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#
# channel.basic_consume(callback,
#                       queue='products11',
#                       no_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()