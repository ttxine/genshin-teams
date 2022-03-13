from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from pydantic import EmailStr

from src.app.auth.jwt import generate_email_confirmation_token
from src.app.user.models import User
from src.config.settings import SITE_DOMAIN

conf = ConnectionConfig(
    MAIL_USERNAME="loremcardstorage@gmail.com",
    MAIL_PASSWORD="gymyba56",
    MAIL_FROM="loremcardstorage@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Genshin Teams",
    MAIL_TLS=True,
    MAIL_SSL=False,
    TEMPLATE_FOLDER='src/templates',
    VALIDATE_CERTS=True
)


async def send_mail(email: EmailStr, subject: str, body: dict, template_name: str):
    message = MessageSchema(
        recipients=[email],
        subject=subject,
        template_body=body,
        subtype='html'
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)


async def send_email_confirmation(user: User):
    token = generate_email_confirmation_token(user.id)
    body = {
        'title': '[Genshin Teams] Confirm E-mail',
        'username': user.username,
        'link': 'http://{0}/confirm-email/?token={1}'.format(SITE_DOMAIN, token)
    }
    await send_mail(user.email, 'Email Confirmation', body, 'email_confirmation.html')


# async def send_password_reset(email: EmailStr):
#     token = create_password_reset_token(email)
#     body = {
#         'title': 'FastAPI Password Reset',
#         'site_domain': SITE_DOMAIN,
#         'confirm_url': '{0}/reset-password/?token={1}'.format(SITE_DOMAIN, token)
#     }
#     await send_mail(email, 'Password Reset', body)
