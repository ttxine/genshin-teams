from fastapi import APIRouter, Depends, Path, Query

from src.app.planner.models import characters as models
from src.app.planner.schemas import characters as schemas
from src.app.planner.services import characters as services


character_router = APIRouter(prefix='/characters', tags=['Characters'])


@character_router.get('', response_model=models.Character)
async def get_character(
    core: int = Query(..., gt=0),
    level: int = Query(..., le=90),
    ascension: int = Query(..., ge=0, le=6),
    weapon: int = Query(..., gt=0)
):
    return await services.CharacterService.get_object_or_404(
        character_core=core,
        level=level,
        ascension=ascension,
        weapon=weapon
    )


@character_router.post('', status_code=201, response_model=models.Character)
async def create_character(schema: schemas.Character):
    return await services.CharacterService.create(schema)


@character_router.put('/{pk}', status_code=201, response_model=models.Character)
async def update_character(schema: schemas.Character, pk: int = Path(...)):
    return await services.CharacterService.update(schema, pk=pk)


@character_router.get('/cores', status_code=201, response_model=list[models.CharacterCore])
async def get_character_cores():
    return await services.CharacterCoreService.all()


@character_router.post('/cores', status_code=201, response_model=models.CharacterCore)
async def create_character_core(schema: schemas.CharacterCoreForm = Depends()):
    return await services.CharacterCoreService.create(schema)
