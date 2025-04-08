import grpc

from app.events.proto import email_pb2_grpc, email_pb2
from app.events.schema import RegisterAndForgotPasswordEmailEvent
from utils.log import logger, trace_id_var


async def send_verification_email_grpc(data: RegisterAndForgotPasswordEmailEvent, queue:str):
    channel = grpc.aio.insecure_channel('localhost:50051')
    stub = email_pb2_grpc.EmailServiceStub(channel)
    request = email_pb2.RegisterAndForgetPasswordEmailRequest(
        trace_id=data.trace_id,
        to=data.to,
        event_name=data.event_name,
        otp=data.otp,
        full_name=data.full_name
    )

    metadata = [("x-api-key", "your-api-key")]

    response = await stub.RegisterSendEmail(request, metadata=metadata)
    if response.success == True:
        logger.info(f"Event sent to Event server, trace_id: {data.trace_id}")
    else:
        logger.exception(f"Exception occured while sending data to event server, trace_id: {data.trace_id}")
