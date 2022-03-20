from fastapi import HTTPException, status


class CredentialsException(HTTPException):

    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers: dict = {'WWW-Authenticate': 'Bearer'}
    ) -> None:
        super().__init__(status_code, detail, headers)


class InvalidTokenException(HTTPException):

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail='Invalid Token',
        headers: dict | None = None
    ) -> None:
        super().__init__(status_code, detail, headers)


class TokenExpiredException(HTTPException):

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail='Token expired',
        headers: dict | None = None
    ) -> None:
        super().__init__(status_code, detail, headers)
