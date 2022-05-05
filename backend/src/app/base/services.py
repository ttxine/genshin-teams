import re
from typing import Any, Type, TypeVar

from ormar import Model
from pydantic import BaseModel
from fastapi import HTTPException

CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


def get_pydantic(model: Type[Model], name: str | None = None, exclude: set | dict = None, include: set | dict = None):
    pydantic = model.get_pydantic(exclude=exclude, include=include)
    if name:
        pydantic.__name__ = name
    return pydantic


class ModelService:
    model: Type[Model]
    create_schema: CreateSchema | None = None
    update_schema: UpdateSchema | None = None

    @classmethod
    async def get(cls, **kwargs) -> Model:
        return await cls.model.objects.get(**kwargs)

    @classmethod
    async def get_or_create(cls, schema: CreateSchema, **kwargs) -> Model:
        obj = await cls.get_object_or_none(**kwargs)
        if obj:
            return obj
        return await cls.create(schema)

    @classmethod
    async def get_object_or_none(cls, **kwargs) -> Type[Model] | None:
        return await cls.model.objects.get_or_none(**kwargs)

    @classmethod
    async def get_object_or_404(cls, **kwargs) -> Model:
        obj = await cls.get_object_or_none(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='{} does not exist'.format(' '.join(re.findall(
                    r'([A-Z][a-z]+)',
                    cls.model.__name__
                )))
            )
        return obj

    @classmethod
    def filter(cls, limit: int | None = None, **kwargs) -> list[Model]:
        qs = cls.model.objects.select_all(follow=True).filter(**kwargs)
        if limit:
            return qs[:limit]
        else:
            return qs

    @classmethod
    async def all(
        cls,
        offset: int | None = None,
        limit: int | None = None,
        **kwargs
    ) -> list[Model]:
        return await cls.model.objects.select_all(follow=True)\
            .offset(offset).limit(limit).all(**kwargs)

    @classmethod
    async def create(cls, schema: CreateSchema | None = None, **kwargs) -> Model:
        if schema:
            model = await cls._pre_save(schema)
            kwargs.update(model)
        return await cls.model.objects.create(**kwargs)

    @classmethod
    async def update(cls, schema: UpdateSchema, **kwargs) -> Model:
        obj = await cls.get_object_or_404(**kwargs)
        model = await cls._pre_save(schema)
        return await obj.update(**model)

    @classmethod
    async def delete(cls, **kwargs):
        return await cls.model.objects.filter(**kwargs).delete()

    @classmethod
    async def exists(cls, **kwargs) -> bool:
        return await cls.model.objects.filter(**kwargs).exists()

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        return schema.dict(exclude_unset=True, exclude_none=exclude_none)
