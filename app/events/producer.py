import aio_pika

from utils.variables import RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_HOST


async def produce(event_data, queue_name):
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/"
    )

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            queue_name,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key=queue_name)

        message = aio_pika.Message(
            body=event_data.encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await exchange.publish(message, routing_key=queue_name)
