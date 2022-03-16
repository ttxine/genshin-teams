from jose import jwt, JWTError

from src.app.auth.models import BlacklistedToken
from src.app.auth.jwt import generate_access_token
from src.config import settings


class Token:

    __slots__ = 'token', 'payload'

    token_type: str
    secret_key: str

    def __init__(self, token: str) -> None:
        self.token = token
        self.payload = jwt.decode(
            token,
            self.secret_key,
            settings.ALGORITHM
        )

    def _get(self, key: str) -> str:
        try:
            val = self.payload[key]
        except KeyError:
            raise JWTError('Token hasn\'t {}'.format(key))
        return val

    def _get_token_type(self) -> str:
        return self._get('token_type')

    def _get_exp(self) -> str:
        return self._get('exp')

    def _get_jti(self) -> str:
        return self._get('jti')

    def _get_sub(self) -> str:
        return self._get('sub')

    @property
    def user_id(self) -> int:
        return int(self._get_sub())

    async def verify(self) -> None:
        self.validate_token_type()
        await self.check_blacklist()

    def validate_token_type(self) -> None:
        token_type = self._get_token_type()
        if self.token_type != token_type:
            raise JWTError('Invalid token type')

    async def is_blacklisted(self) -> bool:
        return await BlacklistedToken.objects.filter(
            user=self._get_sub(),
            jti=self._get_jti()
        ).exists()

    async def blacklist(self) -> BlacklistedToken:
        blacklisted_token = await BlacklistedToken.objects.get_or_create(
            user=self.user_id,
            token=self.token,
            jti=self._get_jti(),
            expires_at=self._get_exp(),
        )
        return blacklisted_token

    async def check_blacklist(self) -> None:
        blacklisted = await self.is_blacklisted()

        if blacklisted:
            raise JWTError('Token is blacklisted')


class AccessToken(Token):
    token_type: str = settings.ACCESS_TOKEN_TYPE
    secret_key: str = settings.ACCESS_TOKEN_SECRET_KEY


class RefreshToken(Token):
    token_type: str = settings.REFRESH_TOKEN_TYPE
    secret_key: str = settings.REFRESH_TOKEN_SECRET_KEY

    def refresh_access_token(self) -> str:
        self.validate_token_type()
        user_id = self.user_id
        return generate_access_token(user_id)


class EmailConfirmationToken(Token):
    token_type: str = settings.EMAIL_CONFIRMATION_TOKEN_TYPE
    secret_key: str = settings.EMAIL_CONFIRMATION_TOKEN_SECRET_KEY


class PasswordResetToken(Token):
    token_type: str = settings.PASSWORD_RESET_TOKEN_TYPE
    secret_key: str = settings.PASSWORD_RESET_TOKEN_SECRET_KEY
