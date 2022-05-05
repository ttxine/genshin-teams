from src.app.base.services import ModelService
from src.app.user.models import User
from src.core.security import get_password_hash


class UserService(ModelService):
    model = User

    @classmethod
    async def confirm(cls, pk: int):
        user: User = await cls.get_object_or_404(pk=pk)
        await user.update(email_confirmed=True)

    @classmethod
    async def create(cls, schema, **kwargs):
        hashed_password = get_password_hash(schema.password)
        return await super().create(
            **schema.dict(exclude={'password'}),
            hashed_password=hashed_password,
            **kwargs
        )


user_service = UserService()
