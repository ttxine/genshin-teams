import re
import asyncio
from typing import Any, Type, TypeVar

import httpx
from ormar import Model

from src.app.planner.models import weapons


Client = TypeVar('Client', bound=httpx.AsyncClient)
Response = TypeVar('Response', bound=httpx.Response)


class GenshinDataCollector:
    url: str
    model: Type[Model]

    @classmethod
    async def collect(cls) -> None:
        response = await cls._get()
        data = response.json()
        await cls._insert_objects(data)
        print('{}s collected successfully'.format(' '.join(re.findall(
            r'([A-Z][a-z]+)',
            cls.model.__name__
        ))).capitalize())

    @classmethod
    async def _get(cls) -> Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(cls.url)
        return response

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any]) -> Type[Model]:
        return cls.model(**raw_obj)

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> list[Type[Model]]:
        for raw_obj in data:
            obj = cls._as_model(raw_obj)
            if obj is not None:
                await cls.model.objects.get_or_create(
                    **obj.dict(exclude={'id'})
                )


class WeaponMainStatDataCollector(GenshinDataCollector):
    url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponExcelConfigData.json'
    model: Type[Model] = weapons.WeaponMainStatCore

    @classmethod
    def _as_model(self, raw_obj: dict[str, Any]) -> Type[Model]:
        rarity = int(raw_obj['RankLevel'])
        raw_rarity = int(raw_obj['WeaponProp'][0]['Type'][-3])
        if rarity > raw_rarity + 2:
            return None
        obj = {}
        obj['rarity'] = rarity
        obj['start_value'] = float(raw_obj['WeaponProp'][0]['InitValue'])
        tier = int(raw_obj['WeaponProp'][0]['Type'][-1])
        if (raw_rarity, tier) in ((2, 3), (3, 3)):
            obj['tier'] = 4
        else:
            obj['tier'] = tier + 1 if tier < 3 else 1
        obj['is_exception'] = False
        return super()._as_model(obj)


class WeaponAscensionValueDataCollector(GenshinDataCollector):
    url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponPromoteExcelConfigData.json'
    model: Type[Model] = weapons.WeaponMainStatAscensionValue

    @classmethod
    def _as_model(self, raw_obj: dict[str, Any]) -> Type[Model]:
        obj = {}
        ascension = raw_obj.get('PromoteLevel')
        if not ascension:
            return None
        obj['ascension'] = ascension
        obj['rarity'] = int(str(raw_obj['WeaponPromoteId'])[2])
        obj['ascension_value'] = float(raw_obj['AddProps'][0]['Value'])
        return super()._as_model(obj)


async def loadgenshindata():
    tasks = [
        WeaponMainStatDataCollector.collect(),
        WeaponAscensionValueDataCollector.collect()
    ]
    await asyncio.gather(*tasks)
