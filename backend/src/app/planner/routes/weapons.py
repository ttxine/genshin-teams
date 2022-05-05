from fastapi import APIRouter, Depends, Query, Security
from src.app.planner.consts import WeaponType

from src.app.planner.schemas import weapons as schemas
from src.app.planner.models import weapons as models
from src.app.planner.services import weapons as services
from src.app.auth.permissions import get_current_superuser

weapon_router = APIRouter(prefix='', tags=['Weapons'])


@weapon_router.get('/weapons/{pk}', response_model=schemas.WeaponR)
async def get_weapon(pk: int):
    weapon: models.Weapon = await services.WeaponService.get_object_or_404(pk=pk)
    pa_stats = await services.WeaponPassiveAbilityStatService.filter(
        core__passive_ability_core=weapon.passive_ability.core,
        refinement=weapon.refinement
    ).all()

    pa = weapon.passive_ability
    pa_schema = schemas.WeaponPassiveAbilityR(**pa.dict(), stats=pa_stats)

    response = weapon.dict(exclude={'passive_ability'})
    response.update(
        passive_ability=pa_schema.dict()
    )

    return response


@weapon_router.post('/weapons', response_model=models.Weapon, status_code=201)
async def create_weapon(
    schema: schemas.Weapon
):
    return await services.WeaponService.get_or_create(
        schema,
        core=schema.core,
        level=schema.level,
        ascension=schema.ascension,
        refinement=schema.refinement
    )


@weapon_router.put('/weapons/{pk}', response_model=models.Weapon, dependencies=[Security(get_current_superuser)])
async def update_weapon(
    pk: int,
    schema: schemas.Weapon
):
    return await services.WeaponService.update(schema, pk=pk)


@weapon_router.get('/weapon-cores', response_model=list[models.WeaponCore], status_code=200)
async def get_weapon_cores(
    weapon_types: list[WeaponType] = Query(...),
    rarities: list[int] = Query(...)
):
    return await services.WeaponCoreService.all(
        weapon_type__in=weapon_types,
        rarity__in=rarities
    )


@weapon_router.post('/weapon-cores', response_model=models.WeaponCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_core(
    schema: schemas.WeaponCoreForm = Depends()
):
    return await services.WeaponCoreService.create(schema)


@weapon_router.post('/weapon-passive-abilities', response_model=models.WeaponPassiveAbility, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability(
    schema: schemas.WeaponPassiveAbilityCU
):
    return await services.WeaponPassiveAbilityService.create(schema)


@weapon_router.post('/weapon-passive-ability-stats', response_model=models.WeaponPassiveAbilityStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat(
    schema: schemas.WeaponPassiveAbilityStat
):
    return await services.WeaponPassiveAbilityStatService.create(schema)


@weapon_router.post('/weapon-passive-ability-cores', response_model=models.WeaponPassiveAbilityCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_core(
    schema: schemas.WeaponPassiveAbilityCore
):
    return await services.WeaponPassiveAbilityCoreService.create(schema)


@weapon_router.post('/weapon-passive-ability-stat-cores', response_model=models.WeaponPassiveAbilityStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat_core(
    schema: schemas.WeaponPassiveAbilityStatCoreCU
):
    return await services.WeaponPassiveAbilityStatCoreService.create(schema)
