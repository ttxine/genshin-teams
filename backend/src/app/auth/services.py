from datetime import datetime
from typing import Type

import ormar
from jose import JWTError
from fastapi import BackgroundTasks, HTTPException, Request, Response, status

from src.core.security import get_password_hash, verify_password
from src.app.user.models import User
from src.app.user.services import user_service
from src.app.user.schemas import UserCreate
from src.app.auth.jwt import generate_refresh_token
from src.app.auth.exceptions import CredentialsException, InvalidTokenException
from src.app.auth.tokens import AccessToken, EmailConfirmationToken, PasswordResetToken, RefreshToken, Token
from src.utils.send_mail import send_email_confirmation, send_password_reset


async def validate_token(raw_token: str, token_class: Type[Token]) -> tuple[int, Token]:
    try:
        token = token_class(raw_token)
        await token.verify()
        user_id = token.user_id
    except JWTError:
        raise InvalidTokenException()
    return user_id, token


async def register_user(schema: UserCreate, task: BackgroundTasks) -> None:
    user_exists = await User.objects.filter(
        ormar.or_(username=user.username, email=user.email)
    ).exists()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with the entered data already exists'
        )
    user = await user_service.create(schema)
    task.add_task(
        send_email_confirmation, user
    )


async def authenticate_user(username: str, raw_password: str) -> User:
    user: User = await user_service.get_object_or_none(username=username)
    if not user or not verify_password(raw_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.email_confirmed and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email not confirmed'
        )
    return user


async def logout_user(token: str, request: Request, response: Response) -> None:
    _, access_token = await validate_token(token, AccessToken)

    refresh_token_cookie = request.cookies.get('rt')
    _, refresh_token = await validate_token(refresh_token_cookie, RefreshToken)

    await access_token.blacklist()
    await refresh_token.blacklist()

    response.delete_cookie(key='rt', secure=True, httponly=True)


async def logout_user_from_all_devices(token: str) -> None:
    user_id, _ = await validate_token(token, AccessToken)
    user = await user_service.get_object_or_404(pk=user_id)

    await user.update(invalidate_before=datetime.utcnow())


async def change_user_password(token: str, old_raw_password: str, new_raw_password: str) -> None:
    user_id, access_token = await validate_token(token, AccessToken)
    user = await user_service.get_object_or_404(pk=user_id)
    if not verify_password(old_raw_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Wrong old password'
        )
    new_hashed_password = get_password_hash(new_raw_password)
    await access_token.blacklist()
    await user.update(
        hashed_password=new_hashed_password,
        invalidate_before=datetime.utcnow()
    )


async def refresh_access_token(token: str, response: Response) -> dict:
    user_id, refresh_token = await validate_token(token, RefreshToken)

    access_token = refresh_token.refresh_access_token()

    await refresh_token.blacklist()
    new_refresh_token = generate_refresh_token(user_id)

    response.set_cookie(key='rt', value=new_refresh_token, httponly=True, secure=True)
    return {'access_token': access_token}


async def confirm_user_email(token: str) -> None:
    user_id, email_confirmation_token = await validate_token(token, EmailConfirmationToken)
    await email_confirmation_token.blacklist()
    await user_service.confirm(pk=user_id)


async def recover_user_password(email: str, task: BackgroundTasks) -> None:
    user = await user_service.get_object_or_404(email=email)
    task.add_task(
        send_password_reset, user
    )


async def reset_user_password(token: str, new_raw_password: str) -> None:
    user_id, password_reset_token = await validate_token(token, PasswordResetToken)
    await password_reset_token.blacklist()
    user: User = await user_service.get_object_or_404(pk=user_id)
    new_hashed_password = get_password_hash(new_raw_password)
    await user.update(
        hashed_password=new_hashed_password,
        invalidate_before=datetime.utcnow()
    )


def get_refresh_token_from_cookie(request: Request) -> str:
    try:
        refresh_token = request.cookies['rt']
    except KeyError:
        raise CredentialsException()
    return refresh_token
