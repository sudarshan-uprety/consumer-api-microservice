from .proto import email_pb2_grpc, email_pb2


class EmailService(email_pb2_grpc.EmailServiceServicer):
    async def SendEmail(self, request, context):
        success = True

        return email_pb2.EmailResponse(
            success=success,
            message="Email sent successfully by server." if success else "Failed to send email"
        )
