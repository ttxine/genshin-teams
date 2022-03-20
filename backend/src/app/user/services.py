import os
from datetime import datetime

from src.app.base.services import BaseService
from src.app.user.models import User
from src.app.user.schemas import UserCreate, UserUpdate
from src.core.security import get_password_hash


class UserService(BaseService):
    model = User
    create_schema = UserCreate
    update_schema = UserUpdate

    @staticmethod
    def _get_avatar_upload_path() -> str:
        directory = 'media/img/users/avatars/{}/'.format(
            str(int(datetime.utcnow().strftime('%d%m%Y'))),
        )
        os.makedirs(directory, exist_ok=True)
        return directory

    async def confirm(self, pk: int):
        user: User = await self.get_object_or_404(pk=pk)
        await user.update(email_confirmed=True)

    async def update(self, schema: UserUpdate, **kwargs):
        avatar = schema.avatar
        if avatar:
            upload_path = self._get_avatar_upload_path()
            image_path = self._upload_image(upload_path, avatar, (250, 250))
            schema.avatar = image_path
        return await super().update(schema, pk=kwargs.get('pk'))

    async def create(self, schema, **kwargs):
        hashed_password = get_password_hash(schema.password)
        return await super().create(
            **schema.dict(exclude={'password'}),
            hashed_password=hashed_password,
            **kwargs
        )


user_service = UserService()
