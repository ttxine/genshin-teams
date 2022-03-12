from typing import Type, TypeVar

from fastapi import HTTPException, UploadFile
from ormar import Model
from pydantic import BaseModel
import aiofiles

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
    async def _upload_file(upload_path: str, file: UploadFile) -> None:
        async with aiofiles.open(upload_path, 'wb') as upload:
            content = await file.read()
            await upload.write(content)
            await upload.close()

    async def get(self, **kwargs) -> GetSchema:
        return await self.model.objects.get(**kwargs)

    async def get_object_or_404(self, **kwargs) -> GetSchema | HTTPException:
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
        return await obj.update(**schema.dict(exclude_unset=True))

    async def delete(self, **kwargs):
        return await self.model.objects.filter(**kwargs).delete()

    async def exists(self, **kwargs) -> bool:
        return await self.model.objects.filter(**kwargs).exists()
