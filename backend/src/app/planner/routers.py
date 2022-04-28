from fastapi import APIRouter
from src.app.planner.routes import weapons
from src.app.planner.routes.artifacts import artifact_router
from src.app.planner.routes.characters import character_router
from src.app.planner.routes.teams import team_router

planner_router = APIRouter()
planner_router.include_router(weapons.weapon_router)
planner_router.include_router(weapons.weapon_passive_ability_router)
planner_router.include_router(weapons.weapon_main_stat_level_multiplier_router)
planner_router.include_router(weapons.weapon_sub_stat_level_multiplier_router)
planner_router.include_router(artifact_router)
planner_router.include_router(character_router)
planner_router.include_router(team_router)
