from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str


class AuthTokens(AccessToken):
    refresh_token: str


class PasswordReset(BaseModel):
    new_password: str


class PasswordChange(PasswordReset):
    old_password: str
