import re
import asyncio
from typing import Any, Type

import httpx
from ormar import Model
from ormar.exceptions import ModelError
from scripts.exceptions import CommandException

from src.app.planner.models import artifacts, weapons, characters

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
    _url: str = None
    _model: Type[Model] = None

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
                'Source url: {1}'.format(e, cls._url)
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
            for roll in range(1, 7):
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


class CharacterLevelMultiplierDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/AvatarCurveExcelConfigData.json'
    _model: Type[Model] = characters.CharacterLevelMultiplier

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_obj in data:
            if raw_obj['Level'] <= 90:
                for rarity_index in range(1, 3):
                    obj = cls._as_model(raw_obj, index=rarity_index)
                    if obj is not None:
                        await cls._model.objects.get_or_create(
                            **obj.dict(exclude={'id'})
                        )

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        obj = {
            'level': raw_obj['Level'],
            'rarity': int(raw_obj['CurveInfos'][kwargs['index']]['Type'][-1]),
            'multiplier': raw_obj['CurveInfos'][kwargs['index']]['Value']
        }
        return super()._as_model(obj)


async def collect_character_ascension():
    ascensions = [
        {
            "ascension": 0,
            "sum_of_sections": 0,
            "bonus_stat_multiplier": 0
        },
        {
            "ascension": 1,
            "sum_of_sections": 38,
            "bonus_stat_multiplier": 0
        },
        {
            "ascension": 2,
            "sum_of_sections": 65,
            "bonus_stat_multiplier": 1
        },
        {
            "ascension": 3,
            "sum_of_sections": 101,
            "bonus_stat_multiplier": 2
        },
        {
            "ascension": 4,
            "sum_of_sections": 128,
            "bonus_stat_multiplier": 2
        },
        {
            "ascension": 5,
            "sum_of_sections": 155,
            "bonus_stat_multiplier": 3
        },
        {
            "ascension": 6,
            "sum_of_sections": 182,
            "bonus_stat_multiplier": 4
        }
    ]

    for ascension in ascensions:
        await characters.CharacterAscension.objects.get_or_create(**ascension)

    print("Character ascension data collected successfully.")


# async def collect_elemental_resonance():
#     resonances = [
#         {
#             "name": "",
#             "effect": {
#                 "stat": "hp",
#                 "value": 0.00
#             },
#         }
#     ]

#     for resonance in resonances:
#         await characters.CharacterAscension.objects.get_or_create(**resonance)

#     print("Character ascension data collected successfully.")


async def loadgenshindata():
    tasks = [
        WeaponMainStatDataCollector.collect(),
        WeaponAscensionValueDataCollector.collect(),
        ArtifactSubStatDataCollector.collect(),
        ArtifactMainStatDataCollector.collect(),
        CharacterLevelMultiplierDataCollector.collect(),
        collect_character_ascension()
    ]
    await asyncio.gather(*tasks)
    print('\nGenshin data has been loaded.')
