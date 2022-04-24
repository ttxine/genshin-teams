from fastapi import APIRouter, Depends, Query, Security

from src.app.planner.schemas import weapons as schemas
from src.app.planner.models import weapons as models
from src.app.planner.services import weapons as services
from src.app.auth.permissions import get_current_superuser

weapon_main_stat_level_multiplier_router = APIRouter(prefix='/weapons', tags=['Level Multipliers'])
weapon_sub_stat_level_multiplier_router = APIRouter(prefix='/weapons', tags=['Level Multipliers'])
weapon_passive_ability_router = APIRouter(prefix='/weapons', tags=['Weapon Passive Abilities'])
weapon_router = APIRouter(prefix='/weapons', tags=['Weapon'])


@weapon_sub_stat_level_multiplier_router.get('/sub-stat-level-multipliers', response_model=list[models.WeaponSubStatLevelMultiplier])
async def get_weapon_sub_stat_level_multiplier():
    return await services.WeaponSubStatLevelMultiplierService().all()


@weapon_sub_stat_level_multiplier_router.post('/sub-stat-level-multipliers', response_model=models.WeaponSubStatLevelMultiplier, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat_level_multiplier(
    schema: models.WeaponSubStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponSubStatLevelMultiplierService().create(schema)


# @weapon_sub_stat_level_multiplier_router.put('/sub-stat-level-multipliers/{pk}', response_model=models.WeaponSubStatLevelMultiplier, dependencies=[Security(get_current_superuser)])
# async def update_weapon_sub_stat_level_multiplier(
#     pk: int,
#     schema: models.WeaponSubStatLevelMultiplier.get_pydantic(exclude={'id'})
# ):
#     return await services.WeaponSubStatLevelMultiplierService().update(schema, pk=pk)


@weapon_passive_ability_router.get('/passive-abilities', response_model=list[models.WeaponPassiveAbility])
async def get_weapon_passive_ability(
    core: int = Query(..., description='ID of passive ability core'),
    refinement: int = Query(..., ge=1, le=5)
):
    return await services.weapon_passive_ability_service.filter(
        core=core,
        refinement=refinement
    ).all()


@weapon_passive_ability_router.post('/passive-abilities', response_model=models.WeaponPassiveAbility, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability(
    schema: schemas.WeaponPassiveAbilityCU
):
    return await services.weapon_passive_ability_service.create(schema)


# @weapon_passive_ability_router.put('/passive-abilities/{pk}', response_model=models.WeaponPassiveAbility, dependencies=[Security(get_current_superuser)])
# async def update_weapon_passive_ability(
#     pk: int,
#     schema: schemas.WeaponPassiveAbilityCU
# ):
#     return await services.weapon_passive_ability_service.update(schema, pk=pk)


@weapon_passive_ability_router.get('/passive-ability-stats', response_model=list[models.WeaponPassiveAbilityStat])
async def get_weapon_passive_ability_stat(
    core: int = Query(..., description='ID of passive ability stat core'),
    refinement: int = Query(..., ge=1, le=5)
):
    return await services.weapon_passive_ability_stat_service.filter(
        core=core,
        refinement=refinement
    ).all()


@weapon_passive_ability_router.post('/passive-ability-stats', response_model=models.WeaponPassiveAbilityStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat(
    schema: schemas.WeaponPassiveAbilityStat
):
    return await services.weapon_passive_ability_stat_service.create(schema)


# @weapon_passive_ability_router.put('/passive-ability-stats/{pk}', response_model=models.WeaponPassiveAbilityStat, dependencies=[Security(get_current_superuser)])
# async def update_weapon_passive_ability_stat(
#     pk: int,
#     schema: schemas.WeaponPassiveAbilityStat
# ):
#     return await services.weapon_passive_ability_stat_service.update(schema, pk=pk)


@weapon_passive_ability_router.get('/passive-ability-cores', response_model=list[models.WeaponPassiveAbilityCore])
async def get_weapon_passive_ability_cores():
    return await services.weapon_passive_ability_core_service.all()


@weapon_passive_ability_router.post('/passive-ability-cores', response_model=models.WeaponPassiveAbilityCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_core(
    schema: schemas.WeaponPassiveAbilityCore
):
    return await services.weapon_passive_ability_core_service.create(schema)


@weapon_passive_ability_router.put('/passive-ability-cores/{pk}', response_model=models.WeaponPassiveAbilityCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_passive_ability_core(
    pk: int,
    schema: schemas.WeaponPassiveAbilityCore
):
    return await services.weapon_passive_ability_core_service.update(schema, pk=pk)


@weapon_passive_ability_router.delete('/passive-ability-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_passive_ability_core(
    pk: int
):
    return await services.weapon_passive_ability_core_service.delete(pk=pk)


@weapon_passive_ability_router.get('/passive-ability-stat-cores', response_model=list[models.WeaponPassiveAbilityStatCore])
async def get_weapon_passive_ability_stat_cores():
    return await services.weapon_passive_ability_stat_core_service.all()


@weapon_passive_ability_router.post('/passive-ability-stat-cores', response_model=models.WeaponPassiveAbilityStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat_core(
    schema: schemas.WeaponPassiveAbilityStatCoreCU
):
    return await services.weapon_passive_ability_stat_core_service.create(schema)


@weapon_passive_ability_router.put('/passive-ability-stat-cores/{pk}', response_model=models.WeaponPassiveAbilityStatCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_passive_ability_stat_core(
    pk: int,
    schema: schemas.WeaponPassiveAbilityStatCoreCU
):
    return await services.weapon_passive_ability_stat_core_service.update(schema, pk=pk)


@weapon_passive_ability_router.delete('/passive-ability-stat-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_passive_ability_stat_core(
    pk: int
):
    return await services.weapon_passive_ability_stat_core_service.delete(pk=pk)


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


# @weapon_router.put('/{pk}', response_model=models.Weapon, dependencies=[Security(get_current_superuser)])
# async def update_weapon(
#     pk: int,
#     schema: schemas.Weapon
# ):
#     return await services.weapon_service.update(schema, pk=pk)


@weapon_router.get('/cores', response_model=list[models.WeaponCore])
async def get_weapon_cores():
    return await services.weapon_core_service.all()


@weapon_router.post('/cores', response_model=models.WeaponCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_core(
    schema: schemas.WeaponCoreForm = Depends()
):
    return await services.weapon_core_service.create(schema)


@weapon_router.put('/cores/{pk}', response_model=models.WeaponCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_core(
    pk: int,
    schema: schemas.WeaponCoreForm = Depends()
):
    return await services.weapon_core_service.update(schema, pk=pk)


@weapon_router.delete('/cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_core(
    pk: int
):
    return await services.weapon_core_service.delete(pk=pk)


@weapon_router.get('/main-stats', response_model=models.WeaponMainStat)
async def get_weapon_main_stat(
    core: int = Query(..., description='ID of main stat core'),
    level: int = Query(..., ge=1, le=90),
    ascension: int = Query(..., ge=0, le=6)
):
    return await services.weapon_main_stat_service.get_object_or_404(
        core=core,
        level=level,
        ascension=ascension
    )


@weapon_router.post('/main-stats', response_model=models.WeaponMainStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat(schema: schemas.WeaponMainStat):
    return await services.weapon_main_stat_service.create(schema)


@weapon_router.post('/main-stat-cores', response_model=models.WeaponMainStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat_core(schema: models.WeaponMainStatCore.get_pydantic(exclude={'id'})):
    return await services.weapon_main_stat_core_service.get_or_create(schema)


# @weapon_router.put('/main-stats/{pk}', response_model=models.WeaponMainStat, dependencies=[Security(get_current_superuser)])
# async def update_weapon_main_stat(
#     pk: int,
#     schema: schemas.WeaponMainStat
# ):
#     return await services.weapon_main_stat_service.update(schema, pk=pk)


@weapon_main_stat_level_multiplier_router.get('/main-stat-level-multipliers', response_model=list[models.WeaponMainStatLevelMultiplier])
async def get_weapon_main_stat_level_multipliers():
    return await services.WeaponMainStatLevelMultiplierService().all()


@weapon_main_stat_level_multiplier_router.post('/main-stat-level-multipliers', response_model=models.WeaponMainStatLevelMultiplier, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat_level_multiplier(
    schema: models.WeaponMainStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponMainStatLevelMultiplierService().create(schema)


# @weapon_main_stat_level_multiplier_router.put('/main-stat-level-multipliers/{pk}', response_model=models.WeaponMainStatLevelMultiplier, dependencies=[Security(get_current_superuser)])
# async def update_weapon_main_stat_level_multiplier(
#     pk: int,
#     schema: models.WeaponMainStatLevelMultiplier.get_pydantic(exclude={'id'})
# ):
#     return await services.WeaponMainStatLevelMultiplierService().update(schema, pk=pk)


@weapon_router.get('/sub-stats', response_model=list[models.WeaponSubStat])
async def get_weapon_sub_stats(
    core: int = Query(..., description='ID of sub stat core'),
    level: int = Query(..., ge=1, le=90)
):
    return await services.weapon_sub_stat_service.fitler(core=core, level=level).all()


@weapon_router.post('/sub-stats', response_model=models.WeaponSubStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat(
    schema: schemas.WeaponSubStat
):
    return await services.weapon_sub_stat_service.create(schema)


# @weapon_router.put('/sub-stats/{pk}', response_model=models.WeaponSubStat, dependencies=[Security(get_current_superuser)])
# async def update_weapon_sub_stat(
#     pk: int,
#     schema: schemas.WeaponSubStat
# ):
#     return await services.weapon_sub_stat_service.update(schema, pk=pk)


# @weapon_router.get('/sub-stat-cores', response_model=list[models.WeaponSubStatCore])
# async def get_weapon_sub_stat_cores():
#     return await services.weapon_sub_stat_core_service.all()


@weapon_router.post('/sub-stat-cores', response_model=models.WeaponSubStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat_core(
    schema: models.WeaponSubStatCore.get_pydantic(exclude={'id'})
):
    return await services.weapon_sub_stat_core_service.create(schema)


# @weapon_router.put('/sub-stat-cores/{pk}', response_model=models.WeaponSubStatCore, dependencies=[Security(get_current_superuser)])
# async def update_weapon_sub_stat_core(
#     pk: int,
#     schema: models.WeaponSubStatCore.get_pydantic(exclude={'id'})
# ):
#     return await services.weapon_sub_stat_core_service.update(schema, pk=pk)


# @weapon_router.delete('/sub-stat-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
# async def delete_weapon_sub_stat_core(
#     pk: int
# ):
#     return await services.weapon_sub_stat_core_service.delete(pk=pk)
