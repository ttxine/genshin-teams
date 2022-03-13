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
    def _get_avatar_upload_path(file_name: str) -> str:
        directory = 'media/img/users/avatars/{}/'.format(
            str(int(datetime.utcnow().strftime('%d%m%Y'))),
        )
        os.makedirs(directory, exist_ok=True)
        return '{0}{1}'.format(directory, file_name)

    async def confirm(self, pk: int):
        user: User = await self.get_object_or_404(pk=pk)
        await user.update(email_confirmed=True)

    async def update(self, schema: UserUpdate, **kwargs):
        avatar = schema.avatar
        if avatar:
            upload_path = self._get_avatar_upload_path(avatar.filename)
            await self._upload_file(upload_path, avatar)
            schema.avatar = upload_path
        return await super().update(schema, pk=kwargs.get('pk'))

    async def create(self, schema, **kwargs):
        hashed_password = get_password_hash(schema.password)
        return await super().create(
            **schema.dict(exclude={'password'}),
            hashed_password=hashed_password
        )


user_service = UserService()
