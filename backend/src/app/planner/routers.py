from fastapi import APIRouter

from src.app.planner.routes.weapons import weapon_router
from src.app.planner.routes.artifacts import artifact_router
from src.app.planner.routes.characters import character_router
from src.app.planner.routes.teams import team_router
from src.app.base.schemas import ExceptionMessage

planner_router = APIRouter(responses={
    201: {'description': 'An item'},
    401: {
        'model': ExceptionMessage,
        'description': 'Bad or expired token'
    },
    403: {
        'model': ExceptionMessage,
        'description': 'Bad request or user doesn\'t have enough '
            'privileges'
    },
    404: {'model': ExceptionMessage}
})
planner_router.include_router(weapon_router)
planner_router.include_router(artifact_router)
planner_router.include_router(character_router)
planner_router.include_router(team_router)
