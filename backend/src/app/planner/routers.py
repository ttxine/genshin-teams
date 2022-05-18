from fastapi import APIRouter

from src.app.base.schemas import ExceptionMessage
from src.app.planner.weapons.routes import weapon_router
from src.app.planner.artifacts.routes import artifact_router

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
