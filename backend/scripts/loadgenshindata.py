import re
import asyncio
from typing import Any, Type

import httpx
from ormar import Model
from ormar.exceptions import ModelError

from scripts.base import Argument, CommandManager
from scripts.exceptions import CommandException
from src.app.planner.weapons import (
    models as weapon_models,
    services as weapon_services,
    schemas as weapon_schemas
)
from src.app.planner.artifacts import models as artifact_models

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

loadgenshindata_manager = CommandManager()


@loadgenshindata_manager.add_command(
    'loadgenshindata',
    description='Loads genshin core data'
)
async def loadgenshindata():
    tasks = [
        WeaponMainStatCoreDataCollector.collect(),
        WeaponSubStatCoreDataCollector.collect(),
        WeaponAscensionValueDataCollector.collect(),
        WeaponLevelMultipliersDataCollector.collect(),
        ArtifactMainStatDataCollector.collect(),
        ArtifactSubStatDataCollector.collect()
    ]
    ready = await asyncio.gather(*tasks)

    if ready:
        post_tasks = [
            collect_weapon_sub_stat(),
            collect_weapon_main_stat()
        ]
        await asyncio.gather(*post_tasks)
    print('\nGenshin data has been loaded.')


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


class WeaponMainStatCoreDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponExcelConfigData.json'
    _model: Type[Model] = weapon_models.WeaponMainStatCore

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        rarity = int(raw_obj['rankLevel'])
        raw_rarity = int(raw_obj['weaponProp'][0]['type'][-3])
        tier = int(raw_obj['weaponProp'][0]['type'][-3:])

        if rarity > raw_rarity + 2:
            return None

        obj = {
            'rarity': rarity,
            'start_value': float(raw_obj['weaponProp'][0]['initValue']),
            'tier': tier,
            'is_exception': False
        }

        return super()._as_model(obj)


class WeaponSubStatCoreDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponExcelConfigData.json'
    _model: Type[Model] = weapon_models.WeaponSubStatCore

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        ingame_prop = raw_obj['weaponProp'][1].get('propType')
        if raw_obj['weaponProp'][1].get('propType'):
            obj = {
                'stat': INGAME_PROPS[ingame_prop],
                'start_value': float(raw_obj['weaponProp'][1]['initValue']),
            }
            return super()._as_model(obj)


class WeaponAscensionValueDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponPromoteExcelConfigData.json'
    _model: Type[Model] = weapon_models.WeaponMainStatAscensionValue

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        ascension = raw_obj.get('promoteLevel')

        if not ascension:
            return None

        obj = {
            'ascension': ascension,
            'rarity': int(str(raw_obj['weaponPromoteId'])[2]),
            'ascension_value': float(raw_obj['addProps'][0]['value'])
        }

        return super()._as_model(obj)


class WeaponLevelMultipliersDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/WeaponCurveExcelConfigData.json'
    _model: Type[Model] = weapon_models.WeaponMainStatLevelMultiplier

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_objs in data:
            if raw_objs['level'] <= 90:
                for raw_obj in raw_objs['curveInfos']:
                    if raw_obj['type'][-10:-4] == 'ATTACK':
                        obj = cls._as_model(raw_obj, level=raw_objs['level'])
                        if obj is not None:
                            await cls._model.objects.get_or_create(
                                **obj.dict(exclude={'id'})
                            )
                    else:
                        await weapon_models.WeaponSubStatLevelMultiplier\
                            .objects.get_or_create(
                                level=raw_objs['level'],
                                multiplier=raw_obj['value']
                            )

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        obj = {
            'tier': int(raw_obj['type'][-3:]),
            'rarity': int(raw_obj['type'][-3]) + 2,
            'multiplier': float(raw_obj['value']),
            'level': kwargs['level']
        }
        return super()._as_model(obj)


async def collect_weapon_main_stat():
    cores = await weapon_models.WeaponMainStatCore.objects.all()
    for core in cores:
        if core.rarity < 3:
            level_range = 71
            ascension_range = 5
        else:
            level_range = 91
            ascension_range = 7
        for level in range(1, level_range):
            for ascension in range(0, ascension_range):
                schema = weapon_schemas.WeaponMainStat(
                    level=level,
                    ascension=ascension,
                    core=core.id
                )
                await weapon_services.WeaponMainStatService.get_or_create(
                    schema,
                    level=level,
                    ascension=ascension,
                    core=core.id
                )

    print('Weapon main stat data has been loaded.')


async def collect_weapon_sub_stat():
    cores = await weapon_models.WeaponSubStatCore.objects.all()
    for core in cores:
        for level in range(1, 91):
            schema = weapon_schemas.WeaponSubStat(
                level=level,
                core=core.id
            )
            await weapon_services.WeaponSubStatService.get_or_create(
                schema,
                level=level,
                core=core.id
            )

    print('Weapon sub stat data has been loaded.')


class ArtifactSubStatDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/ReliquaryAffixExcelConfigData.json'
    _model: Type[Model] = artifact_models.ArtifactSubStat

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_obj in data:
            for roll in range(1, 7):
                raw_obj['roll'] = roll
                obj = cls._as_model(raw_obj)
                if obj is not None:
                    await cls._model.objects.get_or_create(
                        **obj.dict(exclude={'id'})
                    )

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        raw_id = str(raw_obj['id'])
        rarity = int(raw_id[0])

        if rarity < 6:
            prop = raw_obj['propType']
            value = raw_obj['propValue']
            roll = raw_obj['roll']

            obj = {
                'rarity': rarity,
                'stat': INGAME_PROPS[prop],
                'value': value * roll,
                'roll': roll
            }

            return super()._as_model(obj)


class ArtifactMainStatDataCollector(GenshinDataCollector):
    _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/ReliquaryLevelExcelConfigData.json'
    _model: Type[Model] = artifact_models.ArtifactMainStat

    @classmethod
    async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
        for raw_obj in data:
            if raw_obj.get('rank'):
                for prop in raw_obj['addProps']:
                    obj = cls._as_model(
                        prop,
                        rarity=raw_obj['rank'],
                        level=raw_obj['level']
                    )
                    if obj is not None:
                        await cls._model.objects.get_or_create(
                            **obj.dict(exclude={'id'})
                        )

    @classmethod
    def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
        if raw_obj['propType'] not in INGAME_PROPS_EXCLUDE:
            obj = {
                'rarity': kwargs['rarity'],
                'level': kwargs['level'] - 1,
                'stat': INGAME_PROPS[raw_obj['propType']],
                'value': raw_obj['value']
            }
            return super()._as_model(obj)


# class CharacterLevelMultiplierDataCollector(GenshinDataCollector):
#     _url: str = 'https://raw.githubusercontent.com/Dimbreath/GenshinData/master/ExcelBinOutput/AvatarCurveExcelConfigData.json'
#     _model: Type[Model] = characters.CharacterLevelMultiplier

#     @classmethod
#     async def _insert_objects(cls, data: list[dict[str, Any]]) -> None:
#         for raw_obj in data:
#             if raw_obj['level'] <= 90:
#                 for rarity_index in range(1, 3):
#                     obj = cls._as_model(raw_obj, index=rarity_index)
#                     if obj is not None:
#                         await cls._model.objects.get_or_create(
#                             **obj.dict(exclude={'id'})
#                         )

#     @classmethod
#     def _as_model(cls, raw_obj: dict[str, Any], **kwargs) -> Type[Model]:
#         obj = {
#             'level': raw_obj['level'],
#             'rarity': int(raw_obj['curveInfos'][kwargs['index']]['type'][-1]),
#             'multiplier': raw_obj['curveInfos'][kwargs['index']]['value']
#         }
#         return super()._as_model(obj)


# async def collect_character_ascension():
#     ascensions = [
#         {
#             "ascension": 0,
#             "sum_of_sections": 0,
#             "bonus_stat_multiplier": 0
#         },
#         {
#             "ascension": 1,
#             "sum_of_sections": 38,
#             "bonus_stat_multiplier": 0
#         },
#         {
#             "ascension": 2,
#             "sum_of_sections": 65,
#             "bonus_stat_multiplier": 1
#         },
#         {
#             "ascension": 3,
#             "sum_of_sections": 101,
#             "bonus_stat_multiplier": 2
#         },
#         {
#             "ascension": 4,
#             "sum_of_sections": 128,
#             "bonus_stat_multiplier": 2
#         },
#         {
#             "ascension": 5,
#             "sum_of_sections": 155,
#             "bonus_stat_multiplier": 3
#         },
#         {
#             "ascension": 6,
#             "sum_of_sections": 182,
#             "bonus_stat_multiplier": 4
#         }
#     ]

#     for ascension in ascensions:
#         await characters.CharacterAscension.objects.get_or_create(**ascension)

#     print("Character ascension data collected successfully.")


# TODO:
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
