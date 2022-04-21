from fastapi import APIRouter
from src.app.planner.routes import weapons
from src.app.planner.routes.artifacts import artifact_router


weapon_main_router = APIRouter()
weapon_main_router.include_router(weapons.weapon_router)
weapon_main_router.include_router(weapons.weapon_passive_ability_router)
weapon_main_router.include_router(weapons.weapon_main_stat_level_multiplier_router)
weapon_main_router.include_router(weapons.weapon_sub_stat_level_multiplier_router)
