from src.app.base.services import BaseService
from src.app.user.models import User
from src.app.user.schemas import UserCreate, UserOut
from src.core.security import get_password_hash


class UserService(BaseService):
    model = User

    async def get_user_by_username(self, username: str):
        return await User.objects.get_or_none(username=username)

    async def get_user_by_email(self, email: str):
        return await User.objects.get_or_none(email=email)

    async def create(self, schema, **kwargs):
        hashed_password = get_password_hash(schema.password)
        return await super().create(
            **schema.dict(exclude='password'),
            hashed_password=hashed_password
        )


user_service = UserService()
