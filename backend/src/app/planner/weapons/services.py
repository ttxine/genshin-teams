from typing import Any, Type

from ormar import Model

from src.utils.images import upload_image
from src.app.base.uploads import get_weapon_image_upload_path
from src.app.base.services import ModelService, CreateSchema, UpdateSchema
from src.app.planner.weapons import models
from src.app.planner.weapons import schemas


class WeaponMainStatLevelMultiplierService(ModelService):
    model: Type[Model] = models.WeaponMainStatLevelMultiplier


class WeaponMainStatAscensionValueService(ModelService):
    model: Type[Model] = models.WeaponMainStatAscensionValue


class WeaponSubStatLevelMultiplierService(ModelService):
    model: Type[Model] = models.WeaponSubStatLevelMultiplier


class WeaponMainStatCoreService(ModelService):
    model: Type[Model] = models.WeaponMainStatCore


class WeaponMainStatService(ModelService):
    model: Type[Model] = models.WeaponMainStat

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True):
        core: models.WeaponMainStatCore = await WeaponMainStatCoreService\
            .get_object_or_404(pk=schema.core)
        start_value = core.start_value

        rarity = 3 if core.rarity <= 3 else core.rarity
        level_multiplier = await WeaponMainStatLevelMultiplierService\
            .get_object_or_404(
                level=schema.level,
                tier=core.tier,
                rarity=rarity
            )
        if schema.ascension > 0:
            ascension_value = (await WeaponMainStatAscensionValueService\
                .get_object_or_404(
                    ascension=schema.ascension,
                    rarity=core.rarity
                )).ascension_value
        else:
            ascension_value = 0

        value = start_value * level_multiplier.multiplier + ascension_value

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'core'}),
            core=core,
            value=value
        )
        return await super()._pre_save(to_save, exclude_none)


class WeaponSubStatCoreService(ModelService):
    model: Type[Model] = models.WeaponSubStatCore


class WeaponSubStatService(ModelService):
    model: Type[Model] = models.WeaponSubStat

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True):
        core: models.WeaponSubStatCore = await WeaponSubStatCoreService\
            .get_object_or_404(pk=schema.core)

        start_value = core.start_value
        level_multiplier = await WeaponSubStatLevelMultiplierService\
            .get_object_or_404(level=schema.level)

        value = start_value * level_multiplier.multiplier

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'core', 'value'}),
            core=core,
            value=value
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponPassiveAbilityCoreService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbilityCore

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        return schema.dict(exclude={'stat_cores'})

    @classmethod
    async def create(cls, schema: CreateSchema | None = None, **kwargs) -> Model:
        async with cls.model.Meta.database.transaction():
            core = await super().create(schema, **kwargs)
            for stat_core_schema in schema.stat_cores:
                stat_core_schema = schemas.WeaponPassiveAbilityStatCore(
                    **stat_core_schema.dict(),
                    passive_ability_core=core.id
                )
                stat_core = await WeaponPassiveAbilityStatCoreService.create(
                    stat_core_schema
                )
                for refinement in range(1, 6):
                    pas_schema = schemas.WeaponPassiveAbilityStat(
                        core=stat_core.id,
                        refinement=refinement
                    )
                    await WeaponPassiveAbilityStatService.create(pas_schema)
            for refinement in range(1, 6):
                schema = schemas.WeaponPassiveAbilityCU(
                    core=core.id,
                    refinement=refinement
                )
                await WeaponPassiveAbilityService.create(schema)
        return core


class WeaponPassiveAbilityStatCoreService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbilityStatCore
    create_schema: CreateSchema = schemas.WeaponPassiveAbilityStatCoreCU
    update_schema: UpdateSchema = schemas.WeaponPassiveAbilityStatCoreCU

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema):
        passive_ability_core = await WeaponPassiveAbilityCoreService()\
            .get_object_or_404(pk=schema.passive_ability_core)

        refinement_scale = (schema.max_value - schema.start_value) / 4

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(
                exclude={'passive_ability_core', 'refinement_scale'}
            ),
            passive_ability_core=passive_ability_core,
            refinement_scale=refinement_scale
        )

        return await super()._pre_save(to_save)

    @classmethod
    async def get_object_or_none(cls, **kwargs) -> Type[Model] | None:
        return await cls.model.objects.select_related(
            'passive_ability_core'
        ).get_or_none(**kwargs)

    @classmethod
    async def all(cls, limit: int | None = None):
        qs = await cls.model.objects.select_related(
            'passive_ability_core'
        ).all()
        if limit:
            return qs[:limit]
        else:
            return qs

    @classmethod
    def filter(cls, limit: int | None = None, **kwargs):
        qs = cls.model.objects.filter(**kwargs).order_by(
            'position'
        )
        if limit:
            return qs[:limit]
        else:
            return qs


class WeaponPassiveAbilityService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbility

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = False):
        core: models.WeaponPassiveAbilityCore = \
            await WeaponPassiveAbilityCoreService().get_object_or_404(
                id=schema.core
            )

        stat_cores = await WeaponPassiveAbilityStatCoreService().filter(
            passive_ability_core=core
        ).all()

        values = []
        for stat_core in stat_cores:
            stat = await WeaponPassiveAbilityStatService().get_object_or_404(
                refinement=schema.refinement,
                core=stat_core
            )
            values.append(await stat.get_value_display())

        description = core.description_template.format(*values)

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'core', 'description'}),
            core=core,
            description=description
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponPassiveAbilityStatService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbilityStat
    create_schema: CreateSchema = schemas.WeaponPassiveAbilityStat
    update_schema: UpdateSchema = schemas.WeaponPassiveAbilityStat

    @classmethod
    async def get_object_or_none(cls, **kwargs) -> Type[Model] | None:
        return await cls.model.objects.select_related([
            'core'
        ]).get_or_none(**kwargs)

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = False):
        core = await WeaponPassiveAbilityStatCoreService().get_object_or_404(
            pk=schema.core
        )

        value = core.start_value + core.refinement_scale * (
            schema.refinement - 1
        )

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'core', 'value'}),
            core=core,
            value=value
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponCoreService(ModelService):
    model: Type[Model] = models.WeaponCore

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = False):
        fa_img = schema.first_ascension_image
        sa_img = schema.second_ascension_image

        upload_path = get_weapon_image_upload_path(schema.name)
        fa_image_path = upload_image(upload_path, fa_img, (160, 160))

        if sa_img:
            sa_image_path = upload_image(upload_path, sa_img, (160, 160))
        else:
            sa_image_path = None

        main_stat_core = await WeaponMainStatCoreService().get_object_or_404(
            pk=schema.main_stat_core
        )

        sub_stat_core = await WeaponSubStatCoreService().get_object_or_404(
            pk=schema.sub_stat_core
        )

        passive_ability_core = await WeaponPassiveAbilityCoreService()\
            .get_object_or_404(pk=schema.passive_ability_core)

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={
                'first_ascension_image',
                'second_ascension_image',
                'main_stat_core',
                'sub_stat_core',
                'passive_ability_core'
            }),
            first_ascension_image=fa_image_path,
            second_ascension_image=sa_image_path,
            main_stat_core=main_stat_core,
            sub_stat_core=sub_stat_core,
            passive_ability_core=passive_ability_core
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponService(ModelService):
    model: Type[Model] = models.Weapon
    create_schema: CreateSchema = schemas.Weapon
    update_schema: UpdateSchema = schemas.Weapon

    @classmethod
    async def get_object_or_none(cls, **kwargs):
        return await cls.model.objects.select_related([
            'core',
            'main_stat',
            'main_stat__core',
            'sub_stat',
            'sub_stat__core',
            'passive_ability',
            'passive_ability__core',
            'core__main_stat_core',
            'core__sub_stat_core',
            'core__passive_ability_core'
        ]).get_or_none(**kwargs)

    @classmethod
    async def create(cls, schema: CreateSchema | None = None, **kwargs) -> Model:
        weapon = await super().create(schema, **kwargs)
        await weapon.load_all(follow=True)
        return weapon

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True):
        core: models.WeaponCore = await WeaponCoreService().get_object_or_404(
            pk=schema.core
        )

        passive_ability = await WeaponPassiveAbilityService().get_object_or_404(
            core=core,
            refinement=schema.refinement
        )

        main_stat = await WeaponMainStatService().get_object_or_404(
            core=core.main_stat_core,
            level=schema.level,
            ascension=schema.ascension
        )

        sub_stat = await WeaponSubStatService().get_object_or_404(
            core=core.sub_stat_core,
            level=schema.level
        )

        to_save = cls.model(
            **schema.dict(
                exclude={'core', 'main_stat', 'sub_stat', 'passive_ability'}
            ),
            core=core,
            main_stat=main_stat,
            sub_stat=sub_stat,
            passive_ability=passive_ability
        )

        return await super()._pre_save(to_save, exclude_none)
