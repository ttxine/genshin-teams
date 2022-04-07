from fastapi import File, Body, UploadFile
from pydantic import root_validator

from src.app.base.forms import model_form_factory
from src.app.planner.models import weapons

WeaponPassiveAbilityStatFromModel = weapons.WeaponPassiveAbilityStat\
    .get_pydantic(exclude={'id', 'core', 'value'})

WeaponFromModel = weapons.Weapon.get_pydantic(exclude={
    'id',
    'core',
    'main_stat',
    'sub_stat',
    'passive_ability'
})

WeaponPassiveAbilityStatCoreFromModel = weapons.WeaponPassiveAbilityStatCore\
    .get_pydantic(exclude={'id', 'core', 'refinement_scale'})

WeaponPassiveAbilityCore = weapons.WeaponPassiveAbilityCore.get_pydantic(
    exclude={'id'}
)

WeaponPassiveAbilityFromModel = weapons.WeaponPassiveAbility.get_pydantic(
    exclude={'id', 'core', 'passive_ability', 'description'}
)

WeaponCoreFromModel = weapons.WeaponCore.get_pydantic(exclude={
    'id',
    'main_stat_core',
    'sub_stat_core',
    'passive_ability_core',
    'first_ascension_image',
    'second_ascension_image'
})

WeaponSubStatFromModel = weapons.WeaponSubStat.get_pydantic(exclude={
    'id',
    'core',
    'value'
})

WeaponMainStatFromModel = weapons.WeaponMainStat.get_pydantic(exclude={
    'id',
    'core',
    'value'
})


class WeaponSubStat(WeaponSubStatFromModel):
    core: int = Body(
        ...,
        description='ID of sub stat core',
        gt=0
    )


class WeaponMainStat(WeaponMainStatFromModel):
    core: int = Body(
        ...,
        description='ID of main stat core',
        gt=0
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
    main_stat_core: int = Body(
        ...,
        description='ID of main stat core',
        gt=0
    )
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


class WeaponPassiveAbilityR(weapons.WeaponPassiveAbility.get_pydantic()):
    stats: list[weapons.WeaponPassiveAbilityStat.get_pydantic()]


class WeaponR(
    weapons.Weapon.get_pydantic(exclude={
        'passive_ability',
        'core__main_stat_core',
        'core__sub_stat_core',
        'core__passive_ability_core'
    })
):
    passive_ability: WeaponPassiveAbilityR


class Weapon(WeaponFromModel):
    core: int = Body(
        ...,
        description='ID of weapon core',
        gt=0
    )

    @root_validator
    def validate_level_and_ascension(cls, values):
        level, ascension = values.get('level'), values.get('ascension')
        value_error = ValueError('Level doesn\'t match ascension')
        if ascension == 0 and level > 20:
            raise value_error
        elif ascension < 2 and level > 40:
            raise value_error
        elif level > ascension * 10 + 30:
            raise value_error
        return values


WeaponCoreForm = model_form_factory(model=WeaponCoreCU)
# class WeaponPassiveAbilityR(WeaponPassiveAbilityFromModel):
#     passive_ability_stats: list[weapons.WeaponPassiveAbilityStat]
