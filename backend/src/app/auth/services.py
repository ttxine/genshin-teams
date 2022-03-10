from os import access
from fastapi import HTTPException, status
from jose import JWTError, ExpiredSignatureError

from src.app.auth.tokens import AccessToken, RefreshToken
from src.app.user.services import user_service
from src.app.user.schemas import UserCreate
from src.core.security import get_password_hash, verify_password


async def register_user(schema: UserCreate):
    user_exists = await user_service.exists(**schema.dict(exclude={'password'}))
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with these credentials exists'
        )
    user = await user_service.create(schema)
    return user


async def authenticate_user(username: str, raw_password: str):
    user = await user_service.get_object_or_none(username=username)
    if not verify_password(raw_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user


async def change_user_password(token: str, old_raw_password: str, new_raw_password: str) -> None:
    try:
        access_token = AccessToken(token)
        await access_token.verify()
        user_id = access_token.user_id
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token expired',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    user = await user_service.get_object_or_none(pk=user_id)
    if not verify_password(old_raw_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong old password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    new_hashed_password = get_password_hash(new_raw_password)
    await access_token.blacklist()
    await user.update(hashed_password=new_hashed_password)


async def refresh_access_token(token: str):
    credentials_error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        refresh_token = RefreshToken(token)
        token = refresh_token.refresh_access_token()
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token expired',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except JWTError:
        raise credentials_error
    return {'access_token': token}
