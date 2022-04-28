from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response

from src.app.user.models import User
from src.app.auth.permissions import get_current_active_user
from src.app.planner.models import teams as models
from src.app.planner.schemas import teams as schemas
from src.app.planner.services.teams import TeamService


team_router = APIRouter(prefix='/teams', tags=['Teams'])


@team_router.get('', response_model=list[schemas.TeamOut])
async def get_teams(
    offset: int = Query(0),
    limit: int = Query(15)
):
    return await TeamService.all(offset=offset, limit=limit)


@team_router.get('/{pk}', response_model=schemas.TeamOut)
async def get_team(
    pk: int = Path(..., gt=0, description='ID of team')
):
    return await TeamService.get_object_or_404(pk=pk)


@team_router.post('', status_code=201, response_model=schemas.TeamOut)
async def create_team(
    schema: schemas.Team,
    current_user: User = Depends(get_current_active_user)
):
    return await TeamService.create(schema, author=current_user)


@team_router.put('/{pk}', response_model=schemas.TeamOut)
async def update_team(
    schema: schemas.Team,
    pk: int = Path(..., gt=0, description='ID of team'),
    current_user: User = Depends(get_current_active_user)
):
    return await TeamService.update(schema, pk=pk, author=current_user)


@team_router.delete('/{pk}', status_code=204, response_class=Response)
async def delete_team(
    pk: int = Path(..., gt=0, description='ID of team'),
    current_user: User = Depends(get_current_active_user)
):
    team = await TeamService.get_object_or_404(pk=pk)

    if team.author.id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail='Current user doesn\'t have enough privileges'
        )

    await TeamService.delete(pk=pk, author=current_user)
