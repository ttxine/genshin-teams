from pydantic import EmailStr
from fastapi import APIRouter, BackgroundTasks, Request, Response, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.app.auth.jwt import generate_access_token, generate_refresh_token
from src.app.auth.schemas import AccessToken, PasswordChange, PasswordReset, UserCreate, UserLogin
from src.app.auth.services import authenticate_user, change_user_password, confirm_user_email, get_refresh_token_from_cookie, logout_user, logout_user_from_all_devices, recover_user_password, refresh_access_token, register_user, reset_user_password
from src.app.base.schemas import Message
from src.app.auth.permissions import security

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])


@auth_router.post('/register', response_model=Message)
async def register(user: UserCreate, task: BackgroundTasks):
    await register_user(user, task)
    return Message(msg='Email confirmation has been sent')


@auth_router.post('/token', response_model=AccessToken)
async def login(schema: UserLogin, response: Response):
    user = await authenticate_user(schema)

    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    response.set_cookie('rt', refresh_token, secure=True, httponly=True)

    return {'access_token': access_token}


@auth_router.get('/refresh', response_model=AccessToken)
async def refresh(request: Request, response: Response):
    refresh_token = get_refresh_token_from_cookie(request)

    return await refresh_access_token(refresh_token, response)


@auth_router.post('/logout', response_model=Message)
async def logout(
    response: Response,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """
    Убирает из cookie refresh token, access token из памяти
    приложения нужно убрать самостоятельно.
    """
    token = credentials.credentials
    await logout_user(token, request, response)
    return Message(msg='Successful logout')


@auth_router.post('/logout-from-all-devices', response_model=Message)
async def logout_from_all_devices(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    await logout_user_from_all_devices(token)
    return Message(msg='Successful logout from all devices')


@auth_router.post('/change-password', response_model=Message)
async def change_password(
    passwords: PasswordChange,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    await change_user_password(
        token,
        passwords.old_password,
        passwords.new_password
    )
    return Message(msg='Password changed successfully')


@auth_router.post('/confirm-email/{token}', response_model=Message)
async def confirm_email(token: str):
    await confirm_user_email(token)
    return Message(msg='Email confirmed successfully')


@auth_router.post('/recover-password/{email}', response_model=Message)
async def recover_password(email: EmailStr, task: BackgroundTasks):
    await recover_user_password(email, task)
    return Message(msg='Password reset mail has been sent')


@auth_router.post('/reset-password/{token}', response_model=Message)
async def reset_password(token: str, schema: PasswordReset):
    await reset_user_password(token, schema.new_password)
    return Message(msg='Password changed successfully')
