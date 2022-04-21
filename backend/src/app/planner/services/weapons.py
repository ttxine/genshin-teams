from typing import Type

from ormar import Model

from src.app.base.services import ModelService, CreateSchema, UpdateSchema
from src.app.base.uploads import get_weapon_image_upload_path
from src.app.base.utils.images import upload_image
from src.app.planner.models import weapons as models
from src.app.planner.schemas import weapons as schemas


# class WeaponMainStatTierService(ModelService):
#     model: Type[Model] = models.WeaponMainStatTier


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

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = True):
        core: models.WeaponMainStatCore = await WeaponMainStatCoreService().get_object_or_404(
            pk=schema.core
        )
        start_value = core.start_value
        level_multiplier = await WeaponMainStatLevelMultiplierService().get_object_or_404(
            level=schema.level,
            tier=core.tier,
            rarity=core.rarity
        )
        if schema.ascension > 0:
            ascension_value = (await WeaponMainStatAscensionValueService().get_object_or_404(
                ascension=schema.ascension,
                rarity=core.rarity
            )).ascension_value
        else:
            ascension_value = 0

        value = start_value * level_multiplier.multiplier + ascension_value

        ModelSchema = self.model.get_pydantic(exclude={'id'})
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

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = True):
        core: models.WeaponSubStatCore = await WeaponSubStatCoreService().get_object_or_404(
            pk=schema.core
        )
        start_value = core.start_value
        level_multiplier = await WeaponSubStatLevelMultiplierService().get_object_or_404(
            level=schema.level
        )

        value = start_value * level_multiplier.multiplier

        ModelSchema = self.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'core', 'value'}),
            core=core,
            value=value
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponPassiveAbilityCoreService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbilityCore


class WeaponPassiveAbilityStatCoreService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbilityStatCore
    create_schema: CreateSchema = schemas.WeaponPassiveAbilityStatCoreCU
    update_schema: UpdateSchema = schemas.WeaponPassiveAbilityStatCoreCU

    async def _pre_save(self, schema: CreateSchema | UpdateSchema):
        passive_ability_core = await WeaponPassiveAbilityCoreService()\
            .get_object_or_404(pk=schema.passive_ability_core)

        refinement_scale = (schema.max_value - schema.start_value) / 4

        ModelSchema = self.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'passive_ability_core', 'refinement_scale'}),
            passive_ability_core=passive_ability_core,
            refinement_scale=refinement_scale
        )

        return await super()._pre_save(to_save)

    async def get_object_or_none(self, **kwargs) -> Type[Model] | None:
        return await self.model.objects.select_related(
            'passive_ability_core'
        ).get_or_none(**kwargs)

    async def all(self, limit: int | None = None):
        qs = await self.model.objects.select_related(
            'passive_ability_core'
        ).all()
        if limit:
            return qs[:limit]
        else:
            return qs

    def filter(self, limit: int | None = None, **kwargs):
        qs = self.model.objects.filter(**kwargs).order_by(
            'position'
        )
        if limit:
            return qs[:limit]
        else:
            return qs

    async def create(self, schema: schemas.WeaponPassiveAbilityStatCoreCU, **kwargs):
        return await super().create(schema, **kwargs)

    async def update(self, schema: UpdateSchema | None = None, **kwargs):
        return await super().update(schema, **kwargs)


class WeaponPassiveAbilityService(ModelService):
    model: Type[Model] = models.WeaponPassiveAbility
    create_schema = schemas.WeaponPassiveAbilityCU
    update_schema = schemas.WeaponPassiveAbilityCU

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = False):
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

        ModelSchema = self.model.get_pydantic(exclude={'id'})
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

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = False):
        core = await WeaponPassiveAbilityStatCoreService().get_object_or_404(
            pk=schema.core
        )

        value = core.start_value + core.refinement_scale * (schema.refinement - 1)

        ModelSchema = self.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={'core', 'value'}),
            core=core,
            value=value
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponCoreService(ModelService):
    model: Type[Model] = models.WeaponCore

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = False):
        fa_img = schema.first_ascension_image
        sa_img = schema.second_ascension_image

        upload_path = get_weapon_image_upload_path(schema.name)
        fa_image_path = upload_image(upload_path, fa_img, (250, 250))

        if sa_img:
            sa_image_path = upload_image(upload_path, sa_img, (250, 250))
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

        ModelSchema = self.model.get_pydantic(exclude={'id'})
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

    async def _pre_save(self, schema: CreateSchema | UpdateSchema, exclude_none: bool = True):
        core: models.WeaponCore = await WeaponCoreService().get_object_or_404(pk=schema.core)

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

        to_save = self.model(
            **schema.dict(
                exclude={'core', 'main_stat', 'sub_stat', 'passive_ability'}
            ),
            core=core.id,
            main_stat=main_stat.id,
            sub_stat=sub_stat.id,
            passive_ability=passive_ability.id
        )

        return await super()._pre_save(to_save, exclude_none)


weapon_sub_stat_core_service = WeaponSubStatCoreService()
weapon_sub_stat_service = WeaponSubStatService()
weapon_main_stat_core_service = WeaponMainStatCoreService()
weapon_main_stat_service = WeaponMainStatService()
weapon_passive_ability_core_service = WeaponPassiveAbilityCoreService()
weapon_passive_ability_stat_core_service = WeaponPassiveAbilityStatCoreService()
weapon_passive_ability_service = WeaponPassiveAbilityService()
weapon_passive_ability_stat_service = WeaponPassiveAbilityStatService()
weapon_core_service = WeaponCoreService()
weapon_service = WeaponService()
