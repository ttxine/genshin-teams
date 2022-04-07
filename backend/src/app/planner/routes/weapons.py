from fastapi import APIRouter, Depends, Security

from src.app.planner.schemas import weapons as schemas
from src.app.planner.models import weapons as models
from src.app.planner.services import weapons as services
from src.app.auth.permissions import get_current_superuser

weapon_main_stat_level_multiplier_router = APIRouter(tags=['Level Multipliers'])
weapon_sub_stat_level_multiplier_router = APIRouter(tags=['Level Multipliers'])
weapon_main_stat_ascension_value_router = APIRouter(tags=['Ascension Values'])
weapon_passive_ability_router = APIRouter(tags=['Weapon Passive Abilities'])
weapon_main_stat_router = APIRouter(tags=['Weapon Main Stats'])
weapon_router = APIRouter(tags=['Weapon'])
weapon_sub_stat_router = APIRouter(tags=['Weapon Sub Stats'])


@weapon_main_stat_router.get('/weapon-main-stats', response_model=list[models.WeaponMainStat])
async def get_weapon_main_stats():
    return await services.weapon_main_stat_service.all()


@weapon_main_stat_router.post('/weapon-main-stats', response_model=models.WeaponMainStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat(
    schema: schemas.WeaponMainStat
):
    return await services.weapon_main_stat_service.create(schema)


@weapon_main_stat_router.put('/weapon-main-stats/{pk}', response_model=models.WeaponMainStat, dependencies=[Security(get_current_superuser)])
async def update_weapon_main_stat(
    pk: int,
    schema: schemas.WeaponMainStat
):
    return await services.weapon_main_stat_service.update(schema, pk=pk)


@weapon_main_stat_router.delete('/weapon-main-stats/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_main_stat(
    pk: int
):
    return await services.weapon_main_stat_service.delete(pk=pk)


@weapon_main_stat_level_multiplier_router.get('/weapon-main-stat-level-multipliers', response_model=list[models.WeaponMainStatLevelMultiplier])
async def get_weapon_main_stat_level_multipliers():
    return await services.WeaponMainStatLevelMultiplierService().all()


@weapon_main_stat_level_multiplier_router.post('/weapon-main-stat-level-multipliers', response_model=models.WeaponMainStatLevelMultiplier, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_main_stat_level_multiplier(
    schema: models.WeaponMainStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponMainStatLevelMultiplierService().create(schema)


@weapon_main_stat_level_multiplier_router.put('/weapon-main-stat-level-multipliers/{pk}', response_model=models.WeaponMainStatLevelMultiplier, dependencies=[Security(get_current_superuser)])
async def update_weapon_main_stat_level_multiplier(
    pk: int,
    schema: models.WeaponMainStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponMainStatLevelMultiplierService().update(schema, pk=pk)


@weapon_main_stat_level_multiplier_router.delete('/weapon-main-stat-level-multipliers/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_main_stat_level_multiplier(
    pk: int
):
    return await services.WeaponMainStatLevelMultiplierService().delete(pk=pk)


@weapon_sub_stat_router.get('/weapon-sub-stats', response_model=list[models.WeaponSubStat])
async def get_weapon_sub_stats():
    return await services.weapon_sub_stat_service.all()


@weapon_sub_stat_router.post('/weapon-sub-stats', response_model=models.WeaponSubStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat(
    schema: schemas.WeaponSubStat
):
    return await services.weapon_sub_stat_service.create(schema)


@weapon_sub_stat_router.put('/weapon-sub-stats/{pk}', response_model=models.WeaponSubStat, dependencies=[Security(get_current_superuser)])
async def update_weapon_sub_stat(
    pk: int,
    schema: schemas.WeaponSubStat
):
    return await services.weapon_sub_stat_service.update(schema, pk=pk)


@weapon_sub_stat_router.delete('/weapon-sub-stats/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_sub_stat(
    pk: int
):
    return await services.weapon_sub_stat_service.delete(pk=pk)


@weapon_sub_stat_router.get('/weapon-sub-stat-cores', response_model=list[models.WeaponSubStatCore])
async def get_weapon_sub_stat_cores():
    return await services.weapon_sub_stat_core_service.all()


@weapon_sub_stat_router.post('/weapon-sub-stat-cores', response_model=models.WeaponSubStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat_core(
    schema: models.WeaponSubStatCore.get_pydantic(exclude={'id'})
):
    return await services.weapon_sub_stat_core_service.create(schema)


@weapon_sub_stat_router.put('/weapon-sub-stat-cores/{pk}', response_model=models.WeaponSubStatCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_sub_stat_core(
    pk: int,
    schema: models.WeaponSubStatCore.get_pydantic(exclude={'id'})
):
    return await services.weapon_sub_stat_core_service.update(schema, pk=pk)


@weapon_sub_stat_router.delete('/weapon-sub-stat-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_sub_stat_core(
    pk: int
):
    return await services.weapon_sub_stat_core_service.delete(pk=pk)


@weapon_sub_stat_level_multiplier_router.get('/weapon-sub-stat-level-multipliers', response_model=list[models.WeaponSubStatLevelMultiplier])
async def get_weapon_sub_stat_level_multiplier():
    return await services.WeaponSubStatLevelMultiplierService().all()


@weapon_sub_stat_level_multiplier_router.post('/weapon-sub-stat-level-multipliers', response_model=models.WeaponSubStatLevelMultiplier, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_sub_stat_level_multiplier(
    schema: models.WeaponSubStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponSubStatLevelMultiplierService().create(schema)


@weapon_sub_stat_level_multiplier_router.put('/weapon-sub-stat-level-multipliers/{pk}', response_model=models.WeaponSubStatLevelMultiplier, dependencies=[Security(get_current_superuser)])
async def update_weapon_sub_stat_level_multiplier(
    pk: int,
    schema: models.WeaponSubStatLevelMultiplier.get_pydantic(exclude={'id'})
):
    return await services.WeaponSubStatLevelMultiplierService().update(schema, pk=pk)


@weapon_sub_stat_level_multiplier_router.delete('/weapon-sub-stat-level-multipliers/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_sub_stat_level_multiplier(
    pk: int
):
    return await services.WeaponSubStatLevelMultiplierService().delete(pk=pk)


@weapon_passive_ability_router.get('/weapon-passive-abilities', response_model=list[models.WeaponPassiveAbility])
async def get_weapon_passive_abilities():
    return await services.weapon_passive_ability_service.all()


@weapon_passive_ability_router.post('/weapon-passive-abilities', response_model=models.WeaponPassiveAbility, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability(
    schema: schemas.WeaponPassiveAbilityCU
):
    return await services.weapon_passive_ability_service.create(schema)


@weapon_passive_ability_router.put('/weapon-passive-abilities/{pk}', response_model=models.WeaponPassiveAbility, dependencies=[Security(get_current_superuser)])
async def update_weapon_passive_ability(
    pk: int,
    schema: schemas.WeaponPassiveAbilityCU
):
    return await services.weapon_passive_ability_service.update(schema, pk=pk)


@weapon_passive_ability_router.delete('/weapon-passive-abilities/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_passive_ability(
    pk: int
):
    return await services.weapon_passive_ability_service.delete(pk=pk)


@weapon_passive_ability_router.get('/weapon-passive-ability-stats', response_model=list[models.WeaponPassiveAbilityStat])
async def get_weapon_passive_ability_stat():
    return await services.weapon_passive_ability_stat_service.all()


@weapon_passive_ability_router.post('/weapon-passive-ability-stats', response_model=models.WeaponPassiveAbilityStat, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat(
    schema: schemas.WeaponPassiveAbilityStat
):
    return await services.weapon_passive_ability_stat_service.create(schema)


@weapon_passive_ability_router.put('/weapon-passive-ability-stats/{pk}', response_model=models.WeaponPassiveAbilityStat, dependencies=[Security(get_current_superuser)])
async def update_weapon_passive_ability_stat(
    pk: int,
    schema: schemas.WeaponPassiveAbilityStat
):
    return await services.weapon_passive_ability_stat_service.update(schema, pk=pk)


@weapon_passive_ability_router.delete('/weapon-passive-ability-stats/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_passive_ability_stat(
    pk: int
):
    return await services.weapon_passive_ability_stat_service.delete(pk=pk)


@weapon_passive_ability_router.get('/weapon-passive-ability-cores', response_model=list[models.WeaponPassiveAbilityCore])
async def get_weapon_passive_ability_cores():
    return await services.weapon_passive_ability_core_service.all()


@weapon_passive_ability_router.post('/weapon-passive-ability-cores', response_model=models.WeaponPassiveAbilityCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_core(
    schema: schemas.WeaponPassiveAbilityCore
):
    return await services.weapon_passive_ability_core_service.create(schema)


@weapon_passive_ability_router.put('/weapon-passive-ability-cores/{pk}', response_model=models.WeaponPassiveAbilityCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_passive_ability_core(
    pk: int,
    schema: schemas.WeaponPassiveAbilityCore
):
    return await services.weapon_passive_ability_core_service.update(schema, pk=pk)


@weapon_passive_ability_router.delete('/weapon-passive-ability-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_passive_ability_core(
    pk: int
):
    return await services.weapon_passive_ability_core_service.delete(pk=pk)


@weapon_passive_ability_router.get('/weapon-passive-ability-stat-cores', response_model=list[models.WeaponPassiveAbilityStatCore])
async def get_weapon_passive_ability_stat_cores():
    return await services.weapon_passive_ability_stat_core_service.all()


@weapon_passive_ability_router.post('/weapon-passive-ability-stat-cores', response_model=models.WeaponPassiveAbilityStatCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_passive_ability_stat_core(
    schema: schemas.WeaponPassiveAbilityStatCoreCU
):
    return await services.weapon_passive_ability_stat_core_service.create(schema)


@weapon_passive_ability_router.put('/weapon-passive-ability-stat-cores/{pk}', response_model=models.WeaponPassiveAbilityStatCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_passive_ability_stat_core(
    pk: int,
    schema: schemas.WeaponPassiveAbilityStatCoreCU
):
    return await services.weapon_passive_ability_stat_core_service.update(schema, pk=pk)


@weapon_passive_ability_router.delete('/weapon-passive-ability-stat-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_passive_ability_stat_core(
    pk: int
):
    return await services.weapon_passive_ability_stat_core_service.delete(pk=pk)


@weapon_router.get('/', response_model=list[models.Weapon])
async def get_weapon():
    return await services.weapon_service.all()


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


@weapon_router.delete('/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon(
    pk: int
):
    return await services.weapon_service.delete(pk=pk)


@weapon_router.get('/weapon-cores', response_model=list[models.WeaponCore])
async def get_weapon_cores():
    return await services.weapon_core_service.all()


@weapon_router.post('/weapon-cores', response_model=models.WeaponCore, status_code=201, dependencies=[Security(get_current_superuser)])
async def create_weapon_core(
    schema: schemas.WeaponCoreForm = Depends()
):
    return await services.weapon_core_service.create(schema)


@weapon_router.put('/weapon-cores/{pk}', response_model=models.WeaponCore, dependencies=[Security(get_current_superuser)])
async def update_weapon_core(
    pk: int,
    schema: schemas.WeaponCoreForm = Depends()
):
    return await services.weapon_core_service.update(schema, pk=pk)


@weapon_router.delete('/weapon-cores/{pk}', status_code=204, dependencies=[Security(get_current_superuser)])
async def delete_weapon_core(
    pk: int
):
    return await services.weapon_core_service.delete(pk=pk)
