import re
from typing import Any, Type, TypeVar

from ormar import Model
from pydantic import BaseModel
from fastapi import HTTPException

GetSchema = TypeVar('GetSchema', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class ModelService:
    model: Type[Model]
    get_schema: GetSchema | None = None
    create_schema: CreateSchema | None = None
    update_schema: UpdateSchema | None = None

    def __init__(self) -> None:
        if not self.get_schema:
            self.get_schema = self.model
        if not self.create_schema:
            self.create_schema = self.model.get_pydantic(exclude={'id'})
        if not self.update_schema:
            self.update_schema = self.model.get_pydantic(exclude={'id'})

    async def get(self, **kwargs) -> GetSchema:
        return await self.model.objects.get(**kwargs)

    async def get_object_or_none(self, **kwargs) -> Type[Model] | None:
        return await self.model.objects.select_all(follow=True).get_or_none(**kwargs)

    async def get_object_or_404(self, **kwargs) -> GetSchema:
        obj = await self.get_object_or_none(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='{} does not exist'.format(' '.join(re.findall(
                    r'([A-Z][a-z]+)',
                    self.model.__name__
                )))
            )
        return self.get_schema(**obj.dict())

    def filter(self, limit: int | None = None, **kwargs) -> list[GetSchema] | None:
        qs = self.model.objects.select_all(follow=True).filter(**kwargs)
        if limit:
            return qs[:limit]
        else:
            return qs

    async def all(self, limit: int | None = None) -> list[GetSchema] | None:
        qs = await self.model.objects.select_all(follow=True).all()
        if limit:
            return qs[:limit]
        else:
            return qs

    async def create(self, schema: CreateSchema | None = None, **kwargs) -> GetSchema:
        if schema:
            model = await self._pre_save(schema)
            kwargs.update(model)
        return await self.model.objects.create(**kwargs)

    async def update(self, schema: UpdateSchema, **kwargs) -> GetSchema:
        obj = await self.get_object_or_404(**kwargs)
        model = await self._pre_save(schema)
        return await obj.update(**model)

    async def delete(self, **kwargs):
        return await self.model.objects.filter(**kwargs).delete()

    async def exists(self, **kwargs) -> bool:
        return await self.model.objects.filter(**kwargs).exists()

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        return schema.dict(exclude_unset=True, exclude_none=exclude_none)
