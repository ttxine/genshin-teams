from fastapi import File, Body, UploadFile

from src.app.base.forms import model_form_factory
from src.app.planner.models import weapons

WeaponPassiveAbilityStatFromModel = weapons.WeaponPassiveAbilityStat\
    .get_pydantic(exclude={'id', 'core', 'value'})

Weapon = weapons.Weapon.get_pydantic(
    exclude={'id', 'main_stat_value', 'sub_stat_value'}
)

WeaponPassiveAbilityStatCoreFromModel = weapons.WeaponPassiveAbilityStatCore\
    .get_pydantic(exclude={'id', 'core', 'refinement_scale'})

WeaponPassiveAbilityCore = weapons.WeaponPassiveAbilityCore.get_pydantic(
    exclude={'id'}
)

WeaponPassiveAbilityFromModel = weapons.WeaponPassiveAbility.get_pydantic(
    exclude={'id', 'core', 'passive_ability', 'description'}
)

WeaponCoreFromModel = weapons.WeaponCore.get_pydantic(
    exclude={'id', 'sub_stat_core', 'passive_ability_core', 'first_ascension_image', 'second_ascension_image'}
)


class WeaponPassiveAbilityStat(WeaponPassiveAbilityStatFromModel):
    core: int = Body(
        ...,
        description='ID of passive ability stat core',
        gt=0
    )


class WeaponPassiveAbilityStatCoreCU(WeaponPassiveAbilityStatCoreFromModel):
    passive_ability_core: int = Body(
        ...,
        description='ID of passive ability core',
        gt=0
    )


class WeaponPassiveAbilityCU(WeaponPassiveAbilityFromModel):
    core: int = Body(
        ...,
        description='ID of passive ability core',
        gt=0,
    )


class WeaponCoreCU(WeaponCoreFromModel):
    sub_stat_core: int = Body(
        ...,
        description='ID of sub stat core',
        gt=0
    )
    passive_ability_core: int = Body(
        ...,
        description='ID of passive ability core',
        gt=0
    )
    first_ascension_image: UploadFile = File(...)
    second_ascension_image: UploadFile | None = File(None)


WeaponCoreForm = model_form_factory(model=WeaponCoreCU)

# class WeaponPassiveAbilityR(WeaponPassiveAbilityFromModel):
#     passive_ability_stats: list[weapons.WeaponPassiveAbilityStat]
