from getpass import getpass

from src.app.user.services import user_service
from src.app.user.schemas import UserCreate


async def createsuperuser() -> None:
    username = input('Input superuser username: ')
    email = input('Input superuser email: ')
    password = getpass('Input superuser password: ')
    schema = UserCreate(username=username, email=email, password=password)
    username_exists = await user_service.exists(username=username)
    email_exists = await user_service.exists(username=username)
    if username_exists or email_exists:
        print('Superuser with these credentials already exists')
    else:
        await user_service.create(schema, is_superuser=True)
        print('Superuser has been successfully created')
