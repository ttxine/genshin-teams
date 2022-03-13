from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.app.auth.schemas import AuthTokens, AuthUser, AccessToken as AccessTokenSchema, ChangePassword
from src.app.auth.tokens import AccessToken
from src.app.base.schemas import Message
from src.app.user.schemas import UserCreate
from src.app.auth.services import authenticate_user, change_user_password, confirm_user_email, refresh_access_token, register_user
from src.app.auth.jwt import generate_access_token, generate_refresh_token
from src.app.auth.permissions import security

auth_router = APIRouter(tags=['auth'])


@auth_router.post('/register', response_model=Message, status_code=201)
async def register(user_in: UserCreate):
    await register_user(user_in)
    return Message(msg='Email confirmation has been sent')


@auth_router.post('/token', response_model=AuthTokens)
async def login(form_data: AuthUser):
    user = await authenticate_user(
        username=form_data.username,
        raw_password=form_data.password
    )
    user_id = user.id
    access_token = generate_access_token(user_id)
    refresh_token = generate_refresh_token(user_id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


@auth_router.post('/refresh', response_model=AccessTokenSchema)
async def refresh(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    return await refresh_access_token(refresh_token)


@auth_router.post('/logout', response_model=Message)
async def logout(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    access_token = AccessToken(token)
    await access_token.blacklist()
    return Message(msg='Successful logout')


@auth_router.post('/change-password', response_model=Message)
async def change_password(
    passwords: ChangePassword,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    await change_user_password(token, passwords.old_password, passwords.new_password)
    return Message(msg='Password changed successfully')


@auth_router.post('/confirm-email', response_model=Message)
async def confirm_email(token: str):
    await confirm_user_email(token)
    return Message(msg='Email confirmed successfully')
