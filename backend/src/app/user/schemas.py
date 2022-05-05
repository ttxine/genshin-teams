import re
from fastapi import Body, File, UploadFile
from pydantic import BaseModel, EmailStr, validator

from src.app.user.models import User


class UserBase(BaseModel):
    username: str = Body(..., min_length=4, max_length=25)
    email: EmailStr

    @validator('username')
    def validate_username(cls, v: str) -> str:
        if v.isdigit():
            raise ValueError('Username can\'t contain only numbers')
        if not re.match(r'^[\w.@+-]+\Z', v):
            raise ValueError('Username may contain only letters, '
            'numbers, and @/./+/-/_ characters.')
        return v

class UserCreate(UserBase):
    password: str = Body(..., min_length=8, max_length=72)


UserOut = User.get_pydantic(exclude={
    'hashed_password',
    'is_superuser',
    'blacklistedtokens',
    'invalidate_before'
})
