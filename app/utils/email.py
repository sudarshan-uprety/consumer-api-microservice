from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse

from app.utils.templates import templates
from app.models import User
from app.utils.settings import ROOT_URL

conf = ConnectionConfig(
   MAIL_USERNAME='mr.sudarshanuprety@gmail.com',
   MAIL_FROM='mr.sudarshanuprety@gmail.com',
   MAIL_PASSWORD="bujsppzcatxdqvnu",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False
)


async def send_register_mail(user: User, token: str):
    # HTML template for the email body
    template = templates.get_template(f'register.html')
    render_content = template.render(name=f'{user.full_name}', verification_url
                                     =f'{ROOT_URL}/accounts/verify/user/{token}')

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

    # Return response
    return JSONResponse(status_code=200, content={"message": "Email has been sent successfully."})


async def send_forget_password_mail(user: User, token: str):
    # HTML template for the email body
    template = templates.get_template(f'forget_password.html')
    render_content = template.render(name=f'{user.full_name}', verify_link
                                     =f'{ROOT_URL}/accounts/forget/password/{token}')

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

    # Return response
    return JSONResponse(status_code=200, content={"message": "Email has been sent successfully."})
