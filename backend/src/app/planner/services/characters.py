from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from src.utils.images import upload_image
from src.app.base.uploads import get_character_upload_path
from src.app.planner.consts import ArtifactType, Stat
from src.app.planner.models import characters as models
from src.app.planner.models.weapons import Weapon
from src.app.planner.models.artifacts import Artifact
from src.app.base.services import CreateSchema, ModelService, UpdateSchema
from src.app.planner.services.artifacts import ArtifactService
from src.app.planner.services.weapons import (
    WeaponPassiveAbilityStatCoreService,
    WeaponPassiveAbilityStatService,
    WeaponService
)


class CharacterBonusStatCoreService(ModelService):
    model = models.CharacterBonusStatCore


class CharacterBonusStatService(ModelService):
    model = models.CharacterBonusStat


class CharacterLevelMultiplierService(ModelService):
    model = models.CharacterLevelMultiplier


class CharacterAscensionService(ModelService):
    model = models.CharacterAscension


class CharacterCoreService(ModelService):
    model = models.CharacterCore

    @classmethod
    async def all(cls, offset: int | None = None, limit: int | None = None):
        return await cls.model.objects.select_related('bonus_stat_core')\
            .order_by('rarity').all()

    @classmethod
    async def get_object_or_none(cls, **kwargs):
        return await cls.model.objects.select_related('bonus_stat_core').get_or_none(**kwargs)

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        image = schema.image
        upload_path = get_character_upload_path(schema.name)
        image_path = upload_image(upload_path, image, (270, 480))

        bonus_stat_core = await CharacterBonusStatCoreService.get_object_or_none(
            stat=schema.bonus_stat,
            start_value=schema.bonus_stat_start_value
        )
        if not bonus_stat_core:
            bonus_stat_core = await CharacterBonusStatCoreService.create(
                stat=schema.bonus_stat,
                start_value=schema.bonus_stat_start_value
            )

        to_save = cls.model.get_pydantic(exclude={'id'})(
            **schema.dict(exclude={'image'}),
            image=image_path,
            bonus_stat_core=bonus_stat_core
        )
        return await super()._pre_save(to_save, exclude_none)


class CharacterService(ModelService):
    model = models.Character

    @classmethod
    async def get_object_or_none(cls, **kwargs):
        return await cls.model.objects.select_related([
            'character_core',
            'character_core__bonus_stat_core',
            'weapon',
            'weapon__core',
            'weapon__core__main_stat_core',
            'weapon__core__sub_stat_core',
            'weapon__core__passive_ability_core',
            'weapon__main_stat',
            'weapon__main_stat__core',
            'weapon__sub_stat',
            'weapon__sub_stat__core',
            'weapon__passive_ability',
            'weapon__passive_ability__core',
            'bonus_stat',
            'bonus_stat__core',
            'artifact_plume',
            'artifact_sands',
            'artifact_goblet',
            'artifact_circlet',
            'artifact_flower',
        ]).get_or_none(**kwargs)

    @classmethod
    async def _get_artifacts(cls, schema: CreateSchema | UpdateSchema) -> dict[str, Artifact]:
        artifact_flower = await ArtifactService.get_object_or_404(
            pk=schema.artifact_flower,
            core__artifact_type=ArtifactType.FLOWER
        ) if schema.artifact_flower else None
        artifact_plume = await ArtifactService.get_object_or_404(
            pk=schema.artifact_plume,
            core__artifact_type=ArtifactType.PLUME_OF_DEATH
        ) if schema.artifact_plume else None
        artifact_sands = await ArtifactService.get_object_or_404(
            pk=schema.artifact_sands,
            core__artifact_type=ArtifactType.SANDS_OF_EON
        ) if schema.artifact_sands else None
        artifact_goblet = await ArtifactService.get_object_or_404(
            pk=schema.artifact_goblet,
            core__artifact_type=ArtifactType.GOBLET_OF_EONOTHEM
        ) if schema.artifact_goblet else None
        artifact_circlet = await ArtifactService.get_object_or_404(
            pk=schema.artifact_circlet,
            core__artifact_type=ArtifactType.CIRCLET_OF_LOGOS
        ) if schema.artifact_circlet else None
        return {
            'artifact_flower': artifact_flower,
            'artifact_circlet': artifact_circlet,
            'artifact_goblet': artifact_goblet,
            'artifact_plume': artifact_plume,
            'artifact_sands': artifact_sands
        }

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        core: models.CharacterCore = await CharacterCoreService.get_object_or_404(pk=schema.character_core)
        weapon: Weapon = await WeaponService.get_object_or_404(pk=schema.weapon)
        if weapon.core.weapon_type != core.weapon_type:
            raise HTTPException(
                status_code=403,
                detail='Invalid weapon'
            )

        multiplier_obj = await CharacterLevelMultiplierService.get_object_or_404(
            level=schema.level,
            rarity=core.rarity
        )
        ascension_obj = await CharacterAscensionService.get_object_or_404(
            ascension=schema.ascension
        )

        level_multiplier = multiplier_obj.multiplier
        total_section = ascension_obj.sum_of_sections / 182

        health = core.health_start_value * level_multiplier +\
            total_section * core.max_ascension_health
        attack = core.attack_start_value * level_multiplier +\
            total_section * core.max_ascension_attack
        deffence = core.deffence_start_value * level_multiplier +\
            total_section * core.max_ascension_deffence

        total_health = health
        total_attack = attack + weapon.main_stat.value
        total_deffence = deffence
        crit_rate = core.crit_rate_start_value
        crit_damage = core.crit_damage_start_value

        bonus_stat = await CharacterBonusStatService.get_object_or_none(
            core=core,
            ascension=schema.ascension
        )
        if not bonus_stat:
            bonus_stat = await CharacterBonusStatService.create(
                core=core.bonus_stat_core,
                ascension=schema.ascension,
                value=core.bonus_stat_core.start_value / 4 *\
                    ascension_obj.bonus_stat_multiplier
            )
        await bonus_stat.core.load()

        @dataclass
        class StatAdd:
            stat: Stat
            value: int

        const_stats = [
            StatAdd(bonus_stat.core.stat, bonus_stat.value),
            StatAdd(weapon.sub_stat.core.stat, weapon.sub_stat.value)
        ]

        artifacts = await cls._get_artifacts(schema)

        for artifact in artifacts.values():
            if artifact.first_sub_stat:
                const_stats.append(StatAdd(
                    artifact.first_sub_stat.stat,
                    artifact.first_sub_stat.value
                ))
            if artifact.second_sub_stat:
                const_stats.append(StatAdd(
                    artifact.second_sub_stat.stat,
                    artifact.second_sub_stat.value
                ))
            if artifact.third_sub_stat:
                const_stats.append(StatAdd(
                    artifact.third_sub_stat.stat,
                    artifact.third_sub_stat.value
                ))
            if artifact.fourth_sub_stat:
                const_stats.append(StatAdd(
                    artifact.fourth_sub_stat.stat,
                    artifact.fourth_sub_stat.value
                ))

        stat_cores = await WeaponPassiveAbilityStatCoreService.filter(
            passive_ability_core=weapon.passive_ability.core
        ).all()
        for stat_core in stat_cores:
            stat = await WeaponPassiveAbilityStatService.get_object_or_404(
                refinement=weapon.refinement,
                core=stat_core
            )
            if stat.core.stat_type == 'const':
                const_stats.append(StatAdd(stat.core.stat, stat.value))

        character = models.Character.get_pydantic(exclude={'id'})(
            character_core=core,
            level=schema.level,
            ascension=schema.ascension,
            health=health,
            attack=attack,
            deffence=deffence,
            crit_rate=crit_rate,
            crit_damage=crit_damage,
            weapon=weapon,
            bonus_stat=bonus_stat,
            total_health=total_health,
            total_attack=total_attack,
            total_deffence=total_deffence,
            **artifacts
        )

        total_health_flat = 0
        total_health_percentage = 0
        total_attack_flat = 0
        total_attack_percentage = 0
        total_deffence_flat = 0
        total_deffence_percentage = 0

        for stat in const_stats:
            match stat.stat:
                case 'hp':
                    total_health_flat += stat.value
                case 'hp%':
                    total_health_percentage += stat.value
                case 'atk':
                    total_attack_flat += stat.value
                case 'atk%':
                    total_attack_percentage += stat.value
                case 'def':
                    total_deffence_flat += stat.value
                case 'def%':
                    total_deffence_percentage += stat.value
                case 'em':
                    character.elemental_mastery += stat.value
                case 'er%':
                    character.energy_recharge += stat.value
                case 'heal%':
                    character.healing_bonus += stat.value
                case 'cr%':
                    character.crit_rate += stat.value
                case 'cd%':
                    character.crit_damage += stat.value
                case 'elem%':
                    character.geo_damage_bonus += stat.value
                    character.anemo_damage_bonus += stat.value
                    character.cryo_damage_bonus += stat.value
                    character.electro_damage_bonus += stat.value
                    character.hydro_damage_bonus += stat.value
                    character.pyro_damage_bonus += stat.value
                case 'phys%':
                    character.phys_damage_bonus += stat.value
                case 'anemo%':
                    character.anemo_damage_bonus += stat.value
                case 'geo%':
                    character.geo_damage_bonus += stat.value
                case 'electro%':
                    character.electro_damage_bonus += stat.value
                case 'hydro%':
                    character.hydro_damage_bonus += stat.value
                case 'pyro%':
                    character.pyro_damage_bonus += stat.value
                case 'cryo%':
                    character.cryo_damage_bonus += stat.value
                case 'physr%':
                    character.phys_damage_resistance += stat.value
                case 'anemor%':
                    character.anemo_damage_resistance += stat.value
                case 'geor%':
                    character.geo_damage_resistance += stat.value
                case 'electror%':
                    character.electro_damage_resistance += stat.value
                case 'hydror%':
                    character.hydro_damage_resistance += stat.value
                case 'pyror%':
                    character.pyro_damage_resistance += stat.value
                case 'cryor%':
                    character.cryo_damage_resistance += stat.value
                case 'stamina':
                    character.stamina += stat.value
                case 'cdr%':
                    character.cd_reduction += stat.value
                case 'iheal%':
                    character.incoming_healing_bonus += stat.value
                case 'shield%':
                    character.shield_strength += stat.value

        character.total_health = character.total_health *\
            (1 + total_health_percentage) + total_health_flat
        character.total_attack = character.total_attack *\
            (1 + total_attack_percentage) + total_attack_flat
        character.total_deffence = character.total_deffence *\
            (1 + total_deffence_percentage) + total_deffence_flat
        return await super()._pre_save(character, exclude_none)
