from fastapi import Body, UploadFile
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    password: str = Body(..., min_length=8, max_length=72)


class UserLogin(UserBase):
    pass


class UserCreate(UserLogin):
    email: EmailStr


class AccessToken(BaseModel):
    access_token: str


class PasswordReset(BaseModel):
    raw_new_password: str


class PasswordChange(PasswordReset):
    raw_old_password: str
