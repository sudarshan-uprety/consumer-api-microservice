from app.events.producer import produce


async def email_verification_procedure(data, queue):
    await produce(event_data=data, queue_name=queue)


async def forget_password_verification_procedure(data, queue):
    await produce(event_data=data, queue_name=queue)
