from fastapi import Body, File, UploadFile
from pydantic import BaseModel, EmailStr

from src.app.user.models import User


class UserBase(BaseModel):
    username: str = Body(..., min_length=4, max_length=25)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Body(..., min_length=8, max_length=72)


class UserUpdate(BaseModel):
    avatar: UploadFile | None = File(None)


UserOut = User.get_pydantic(exclude={
    'hashed_password',
    'is_superuser',
    'blacklistedtokens'
})
