from typing import Type, TypeVar

from ormar import Model
from pydantic import BaseModel
from fastapi import HTTPException

GetSchema = TypeVar('GetSchema', bound=BaseModel)


class BaseService:
    model: Type[Model]
    get_schema: GetSchema | None = None

    def __init__(self) -> None:
        if not self.get_schema:
            self.get_schema = self.model

    async def get(self, **kwargs):
        return await self.model.objects.get(**kwargs)

    async def get_object_or_none(self, **kwargs) -> GetSchema | None:
        obj = await self.model.objects.get_or_none(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='{} does not exist'.format(self.model.__name__)
            )
        return self.get_schema(**obj.dict())

    async def all(self) -> GetSchema | None:
        return await self.model.objects.all()

    async def create(self, schema: Type[BaseModel] | None, **kwargs) -> GetSchema:
        obj = await self.model.objects.create(
            **schema.dict(exclude_unset=True),
            **kwargs
        )
        return self.get_schema(**obj.dict())

    async def update(self, schema: Type[BaseModel] | None, **kwargs) -> GetSchema | None:
       return await self.model.objects.filter(**kwargs)\
           .update(**schema.dict()).save()

    async def delete(self, **kwargs):
        return await self.model.objects.filter(**kwargs).delete()

    async def exists(self, **kwargs) -> bool:
        return await self.model.objects.filter(**kwargs).exists()
