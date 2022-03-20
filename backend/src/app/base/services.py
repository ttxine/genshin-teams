import os
import string
from random import sample
from typing import Type, TypeVar

from ormar import Model
from pydantic import BaseModel
from fastapi import HTTPException, UploadFile

from src.config import settings
from src.app.base.utils.images import resize_image

GetSchema = TypeVar('GetSchema', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseService:
    model: Type[Model]
    get_schema: GetSchema | None = None
    create_schema: CreateSchema
    update_schema: UpdateSchema

    def __init__(self) -> None:
        if not self.get_schema:
            self.get_schema = self.model

    @staticmethod
    def _upload_image(
        upload_path: str,
        file: UploadFile,
        size = tuple[int, int]
    ) -> str:
        filename, extension = file.filename.split('.')

        if extension not in settings.ALLOWED_FORMAT_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail='Forbidden file format. '
                'Allowed format extensions are {}'.format(
                    settings.ALLOWED_FORMAT_EXTENSIONS
                )
            )

        image = resize_image(file.file, size)
        image = image.convert('RGB')

        image_path = '{0}{1}.jpeg'.format(upload_path, filename)
        if os.path.exists(image_path):
            image_path = '{0}{1}_{2}.jpeg'.format(
                upload_path,
                filename,
                ''.join(sample(string.ascii_letters, 10))
            )

        image.save(image_path, 'JPEG', quality=95)
        return image_path

    async def get(self, **kwargs) -> GetSchema:
        return await self.model.objects.get(**kwargs)

    async def get_object_or_none(self, **kwargs):
        return await self.model.objects.get_or_none(**kwargs)

    async def get_object_or_404(self, **kwargs) -> GetSchema:
        obj = await self.model.objects.get_or_none(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='{} does not exist'.format(self.model.__name__)
            )
        return self.get_schema(**obj.dict())

    async def all(self) -> GetSchema | None:
        return await self.model.objects.all()

    async def create(
        self,
        schema: CreateSchema | None = None,
        **kwargs
    ) -> GetSchema:
        if schema:
            kwargs.update(schema.dict(exclude_unset=True))
        obj = await self.model.objects.create(**kwargs)
        return self.get_schema(**obj.dict())

    async def update(
        self,
        schema: UpdateSchema | None = None,
        **kwargs
    ) -> GetSchema:
        obj = await self.model.objects.get(**kwargs)
        return await obj.update(
            **schema.dict(exclude_unset=True, exclude_none=True)
        )

    async def delete(self, **kwargs):
        return await self.model.objects.filter(**kwargs).delete()

    async def exists(self, **kwargs) -> bool:
        return await self.model.objects.filter(**kwargs).exists()
