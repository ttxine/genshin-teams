from pydantic import BaseModel


class AuthUser(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str


class AuthTokens(AccessToken):
    refresh_token: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
