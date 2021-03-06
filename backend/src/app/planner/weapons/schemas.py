from pydantic import root_validator
from fastapi import File, Body, UploadFile

from src.app.base.forms import model_form_factory
from src.app.planner.weapons import models

WeaponPassiveAbilityStatFromModel = models.WeaponPassiveAbilityStat\
    .get_pydantic(exclude={'id', 'core', 'value'})
WeaponFromModel = models.Weapon.get_pydantic(exclude={
    'id',
    'core',
    'main_stat',
    'sub_stat',
    'passive_ability'
})
WeaponPassiveAbilityStatCoreCU = models.WeaponPassiveAbilityStatCore\
    .get_pydantic(
        exclude={'id', 'core', 'refinement_scale', 'passive_ability_core'}
    )

WeaponPassiveAbilityFromModel = models.WeaponPassiveAbility.get_pydantic(
    exclude={'id', 'core', 'description'}
)
WeaponCoreFromModel = models.WeaponCore.get_pydantic(exclude={
    'id',
    'main_stat_core',
    'sub_stat_core',
    'passive_ability_core',
    'first_ascension_image',
    'second_ascension_image'
})
WeaponSubStatFromModel = models.WeaponSubStat.get_pydantic(exclude={
    'id',
    'core',
    'value'
})
WeaponMainStatFromModel = models.WeaponMainStat.get_pydantic(exclude={
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


class WeaponPassiveAbilityStatCore(WeaponPassiveAbilityStatCoreCU):
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


class WeaponPassiveAbilityR(models.WeaponPassiveAbility.get_pydantic()):
    stats: list[models.WeaponPassiveAbilityStat.get_pydantic()]


class WeaponR(models.Weapon.get_pydantic(exclude={'passive_ability'})):
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
        elif ascension == 1 and (level > 40 or level < 20):
            raise value_error
        elif (ascension > 1 and
            (level > ascension * 10 + 30 or level < ascension * 10 + 20)):
            raise value_error
        return values


class WeaponPassiveAbilityCore(models.WeaponPassiveAbilityCore.get_pydantic(
    exclude={'id'}
)):
    stat_cores: list[WeaponPassiveAbilityStatCoreCU]


WeaponCoreForm = model_form_factory(model=WeaponCoreCU)
