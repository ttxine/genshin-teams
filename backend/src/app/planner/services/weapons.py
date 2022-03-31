from typing import Type

from ormar import Model

from src.app.base.services import ModelService, CreateSchema, UpdateSchema
from src.app.base.uploads import get_weapon_image_upload_path
from src.app.base.utils.images import upload_image
from src.app.planner.models import weapons as models
from src.app.planner.schemas import weapons as schemas


class WeaponMainStatTierService(ModelService):
    model: Type[Model] = models.WeaponMainStatTier


class WeaponMainStatLevelMultiplierService(ModelService):
    model: Type[Model] = models.WeaponMainStatLevelMultiplier


class WeaponMainStatAscensionValueService(ModelService):
    model: Type[Model] = models.WeaponMainStatAscensionValue


class WeaponSubStatLevelMultiplierService(ModelService):
    model: Type[Model] = models.WeaponSubStatLevelMultiplier


class WeaponSubStatCoreService(ModelService):
    model: Type[Model] = models.WeaponSubStatCore


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
                'sub_stat_core',
                'passive_ability_core'
            }),
            first_ascension_image=fa_image_path,
            second_ascension_image=sa_image_path,
            sub_stat_core=sub_stat_core,
            passive_ability_core=passive_ability_core
        )

        return await super()._pre_save(to_save, exclude_none)


class WeaponService(ModelService):
    model: Type[Model] = models.Weapon
    create_schema: CreateSchema = schemas.Weapon
    update_schema: UpdateSchema = schemas.Weapon


weapon_passive_ability_core_service = WeaponPassiveAbilityCoreService()
weapon_passive_ability_stat_core_service = WeaponPassiveAbilityStatCoreService()
weapon_passive_ability_service = WeaponPassiveAbilityService()
weapon_passive_ability_stat_service = WeaponPassiveAbilityStatService()
weapon_core_service = WeaponCoreService()
weapon_sub_stat_core_service = WeaponSubStatCoreService()
