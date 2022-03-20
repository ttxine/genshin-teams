from jose import JWTError, ExpiredSignatureError
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.app.auth.exceptions import CredentialsException, TokenExpiredException

from src.app.auth.tokens import AccessToken
from src.app.user.services import user_service
from src.app.user.models import User


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> User:
    token = credentials.credentials
    try:
        access_token = AccessToken(token)
        await access_token.verify()
        user_id = access_token.user_id
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except JWTError:
        raise CredentialsException()
    user = await user_service.get_object_or_404(pk=user_id)
    return user


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user',
        )
    return user
