import re
import asyncio
from typing import Any, Type

import httpx
from ormar import Model
from ormar.exceptions import ModelError
from scripts.exceptions import CommandException

from src.app.planner.models import artifacts, weapons

INGAME_PROPS = {
    'FIGHT_PROP_HP': 'hp',
    'FIGHT_PROP_HP_PERCENT': 'hp%',
    'FIGHT_PROP_ATTACK': 'atk',
    'FIGHT_PROP_ATTACK_PERCENT': 'atk%',
    'FIGHT_PROP_DEFENSE': 'def',
    'FIGHT_PROP_DEFENSE_PERCENT': 'def%',
    'FIGHT_PROP_CRITICAL': 'cr%',
    'FIGHT_PROP_CRITICAL_HURT': 'cd%',
    'FIGHT_PROP_ELEMENT_MASTERY': 'em',
    'FIGHT_PROP_CHARGE_EFFICIENCY': 'er%',
    'FIGHT_PROP_HEAL_ADD': 'heal%',
    'FIGHT_PROP_FIRE_ADD_HURT': 'elem%',
    'FIGHT_PROP_PHYSICAL_ADD_HURT': 'phys%'
}

INGAME_PROPS_EXCLUDE = {
    'FIGHT_PROP_ELEC_ADD_HURT',
    'FIGHT_PROP_WATER_ADD_HURT',
    'FIGHT_PROP_WIND_ADD_HURT',
    'FIGHT_PROP_ROCK_ADD_HURT',
    'FIGHT_PROP_GRASS_ADD_HURT',
    'FIGHT_PROP_ICE_ADD_HURT',
    'FIGHT_PROP_FIRE_SUB_HURT'
}


class GenshinDataCollector:
    _url: str
    _model: Type[Model]

    @classmethod
    async def collect(cls) -> None:
        response = await cls._get()
        data = response.json()

        try:
            await cls._insert_objects(data)
        except ModelError as e:
            raise CommandException(
                'Genshin data could not be loaded.\nError: {}.'.format(e)
            ) from ModelError
        except KeyError as e:
            raise CommandException(
                'Genshin data could not be loaded.\nError: Raw object from '
                'data source doesn\'t have {0} key. '
                'Source _url: {1}'.format(e, cls._url)
            ) from KeyError
        else:
            print('{}s collected successfully.'.format(' '.join(re.findall(
                    r'([A-Z][a-z]+)',cls._model.__name__))).capitalize())

    @classmethod
    async def _get(cls) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(cls._url)
        return response

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        return cls._model(**raw_obj, **kwargs)

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_obj in data:
            obj = cls._as_model(raw_obj)
            if obj is not None:
                await cls._model.objects.get_or_create(
                    **obj.dict(exclude={'id'})
                )


class WeaponMainStatDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponExcelConfigData.json'
    _model: Type[Model] = weapons.WeaponMainStatCore

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        rarity = int(raw_obj['RankLevel'])
        raw_rarity = int(raw_obj['WeaponProp'][0]['Type'][-3])
        raw_tier = int(raw_obj['WeaponProp'][0]['Type'][-1])

        if rarity > raw_rarity + 2:
            return None

        if (raw_rarity, raw_tier) in ((2, 3), (3, 3)):
            tier = 4
        else:
            tier = raw_tier + 1 if raw_tier < 3 else 1

        obj = {
            'rarity': rarity,
            'start_value': float(raw_obj['WeaponProp'][0]['InitValue']),
            'tier': tier,
            'is_exception': False
        }

        return super()._as_model(obj)


class WeaponAscensionValueDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponPromoteExcelConfigData.json'
    _model: Type[Model] = weapons.WeaponMainStatAscensionValue

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        ascension = raw_obj.get('PromoteLevel')

        if not ascension:
            return None

        obj = {
            'ascension': ascension,
            'rarity': int(str(raw_obj['WeaponPromoteId'])[2]),
            'ascension_value': float(raw_obj['AddProps'][0]['Value'])
        }

        return super()._as_model(obj)


class ArtifactSubStatDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/ReliquaryAffixExcelConfigData.json'
    _model: Type[Model] = artifacts.ArtifactSubStat

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_obj in data:
            for roll in range(1, 5):
                raw_obj['Roll'] = roll
                obj = cls._as_model(raw_obj)
                if obj is not None:
                    await cls._model.objects.get_or_create(
                        **obj.dict(exclude={'id'})
                    )

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        raw_id = str(raw_obj['Id'])
        rarity = int(raw_id[0])

        if rarity < 6:
            prop = raw_obj['PropType']
            value = raw_obj['PropValue']
            roll = raw_obj['Roll']

            obj = {
                'rarity': rarity,
                'stat': INGAME_PROPS[prop],
                'value': value * roll,
                'roll': roll
            }

            return super()._as_model(obj)


class ArtifactMainStatDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/ReliquaryLevelExcelConfigData.json'
    _model: Type[Model] = artifacts.ArtifactMainStat

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_obj in data:
            if raw_obj.get('Rank'):
                for prop in raw_obj['AddProps']:
                    obj = cls._as_model(prop, rarity=raw_obj['Rank'], level=raw_obj['Level'])
                    if obj is not None:
                        await cls._model.objects.get_or_create(
                            **obj.dict(exclude={'id'})
                        )

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        if raw_obj['PropType'] not in INGAME_PROPS_EXCLUDE:
            obj = {
                'rarity': kwargs['rarity'],
                'level': kwargs['level'] - 1,
                'stat': INGAME_PROPS[raw_obj['PropType']],
                'value': raw_obj['Value']
            }
            return super()._as_model(obj)


async def loadgenshindata():
    tasks = [
        WeaponMainStatDataCollector.collect(),
        WeaponAscensionValueDataCollector.collect(),
        ArtifactSubStatDataCollector.collect(),
        ArtifactMainStatDataCollector.collect()
    ]
    await asyncio.gather(*tasks)
    print('\nGenshin data has been loaded.')
