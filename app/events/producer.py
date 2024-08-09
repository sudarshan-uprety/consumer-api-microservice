import pika

from utils.variables import RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_HOST, INVENTORY_QUEUE


def inventory_produce(event_data):
    credentials = pika.PlainCredentials(
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials)
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange=INVENTORY_QUEUE,
        durable=True,
        exchange_type='topic'
    )

    # Declare and bind queue INVENTORY_QUEUE
    channel.queue_declare(queue=INVENTORY_QUEUE, durable=True)
    channel.queue_bind(
        exchange=INVENTORY_QUEUE,
        queue=INVENTORY_QUEUE,
        routing_key=INVENTORY_QUEUE
    )
    # publish the data for subscriber
    channel.basic_publish(
        exchange=INVENTORY_QUEUE,
        routing_key=INVENTORY_QUEUE,
        body=event_data,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
