from fastapi import APIRouter, Depends, Query, Security

from src.app.planner.schemas import weapons as schemas
from src.app.planner.models import weapons as models
from src.app.planner.services import weapons as services
from src.app.auth.permissions import get_current_superuser

weapon_main_stat_level_multiplier_router = APIRouter(prefix='/weapons', tags=['Level Multipliers'])
weapon_sub_stat_level_multiplier_router = APIRouter(prefix='/weapons', tags=['Level Multipliers'])
weapon_passive_ability_router = APIRouter(prefix='/weapons', tags=['Weapon Passive Abilities'])
weapon_router = APIRouter(prefix='/weapons', tags=['Weapons'])


@weapon_sub_stat_level_multiplier_router.post('/sub-stat-level-multipliers', response_model=models.WeaponSubStatLevelMultiplier, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat_level_multiplier(
    schema: models.WeaponSubStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponSubStatLevelMultiplierService().create(schema)


@weapon_passive_ability_router.post('/passive-abilities', response_model=models.WeaponPassiveAbility, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability(
    schema: schemas.WeaponPassiveAbilityCU
):
    return await services.weapon_passive_ability_service.create(schema)


@weapon_passive_ability_router.post('/passive-ability-stats', response_model=models.WeaponPassiveAbilityStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat(
    schema: schemas.WeaponPassiveAbilityStat
):
    return await services.weapon_passive_ability_stat_service.create(schema)


@weapon_passive_ability_router.post('/passive-ability-cores', response_model=models.WeaponPassiveAbilityCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_core(
    schema: schemas.WeaponPassiveAbilityCore
):
    return await services.weapon_passive_ability_core_service.create(schema)


@weapon_passive_ability_router.post('/passive-ability-stat-cores', response_model=models.WeaponPassiveAbilityStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat_core(
    schema: schemas.WeaponPassiveAbilityStatCoreCU
):
    return await services.weapon_passive_ability_stat_core_service.create(schema)


@weapon_router.get('/{pk}', response_model=schemas.WeaponR)
async def get_weapon(pk: int):
    weapon: models.Weapon = await services.weapon_service.get_object_or_404(pk=pk)
    pa_stats = await services.weapon_passive_ability_stat_service.filter(
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


@weapon_router.post('/', response_model=models.Weapon, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon(
    schema: schemas.Weapon
):
    return await services.weapon_service.create(schema)


@weapon_router.put('/{pk}', response_model=models.Weapon, dependencies=[Security(get_current_superuser)])
async def update_weapon(
    pk: int,
    schema: schemas.Weapon
):
    return await services.weapon_service.update(schema, pk=pk)


@weapon_router.post('/cores', response_model=models.WeaponCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_core(
    schema: schemas.WeaponCoreForm = Depends()
):
    return await services.weapon_core_service.create(schema)


@weapon_router.post('/main-stats', response_model=models.WeaponMainStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat(schema: schemas.WeaponMainStat):
    return await services.weapon_main_stat_service.create(schema)


@weapon_router.post('/main-stat-cores', response_model=models.WeaponMainStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat_core(schema: models.WeaponMainStatCore.get_pydantic(exclude={'id'})):
    return await services.weapon_main_stat_core_service.get_or_create(schema)


@weapon_main_stat_level_multiplier_router.post('/main-stat-level-multipliers', response_model=models.WeaponMainStatLevelMultiplier, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat_level_multiplier(
    schema: models.WeaponMainStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponMainStatLevelMultiplierService().create(schema)


@weapon_router.post('/sub-stats', response_model=models.WeaponSubStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat(
    schema: schemas.WeaponSubStat
):
    return await services.weapon_sub_stat_service.create(schema)


@weapon_router.post('/sub-stat-cores', response_model=models.WeaponSubStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat_core(
    schema: models.WeaponSubStatCore.get_pydantic(exclude={'id'})
):
    return await services.weapon_sub_stat_core_service.create(schema)
