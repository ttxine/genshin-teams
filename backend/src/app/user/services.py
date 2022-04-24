from src.app.base.services import ModelService
from src.app.base.uploads import get_avatar_upload_path
from src.utils.images import upload_image
from src.app.user.models import User
from src.app.user.schemas import UserCreate, UserUpdate
from src.core.security import get_password_hash


class UserService(ModelService):
    model = User
    create_schema = UserCreate
    update_schema = UserUpdate

    @classmethod
    async def confirm(cls, pk: int):
        user: User = await cls.get_object_or_404(pk=pk)
        await user.update(email_confirmed=True)

    @classmethod
    async def update(cls, schema: UserUpdate, **kwargs):
        avatar = schema.avatar
        if avatar:
            upload_path = get_avatar_upload_path()
            image_path = upload_image(upload_path, avatar, (250, 250))
            schema.avatar = image_path
        return await super().update(schema, pk=kwargs.get('pk'))

    @classmethod
    async def create(cls, schema, **kwargs):
        hashed_password = get_password_hash(schema.password)
        return await super().create(
            **schema.dict(exclude={'password'}),
            hashed_password=hashed_password,
            **kwargs
        )


user_service = UserService()
