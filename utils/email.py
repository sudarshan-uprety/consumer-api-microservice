from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.user.models import Users
from utils.templates import templates
from utils.variables import *

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_FROM=MAIL_FROM,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)


async def send_register_mail(user: Users, otp: str):
    # HTML template for the email body
    template = templates.get_template(f'register.html')
    render_content = template.render(name=f'{user.full_name}', otp=otp)
    # Create message schema
    message = MessageSchema(
        subject="Verification email",
        recipients=[user.email],  # List of recipients
        body=render_content,
        subtype="html"
    )

    # Send email using FastAPI-Mail
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_forget_password_mail(user: Users, code: str):
    # HTML template for the email body
    template = templates.get_template(f'forget_password.html')
    render_content = template.render(
        name=f'{user.full_name}',
        otp=code
    )

    # Create message schema
    message = MessageSchema(
        subject="Verification email",
        recipients=[user.email],  # List of recipients
        body=render_content,
        subtype="html"
    )

    # Send email using FastAPI-Mail
    fm = FastMail(conf)
    await fm.send_message(message)
