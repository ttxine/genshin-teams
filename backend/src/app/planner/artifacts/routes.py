from fastapi import APIRouter, Depends, HTTPException, Path, Query, Security

from src.app.auth.permissions import get_current_superuser
from src.app.planner.consts import (
    ALLOWED_ARTIFACT_MAIN_STATS_FOR_TYPE,
    ArtifactType,
    Stat
)
from src.app.planner.artifacts import models, schemas, services

artifact_router = APIRouter(tags=['Artifacts'])


@artifact_router.get('/artifacts', response_model=list[models.Artifact])
async def get_artifacts(artifact_set: int = Query(..., description='ID of artifact set')):
    return await services.ArtifactService.filter(
        core__artifact_set=artifact_set
    ).all()


@artifact_router.get('/artifacts/{pk}', response_model=models.Artifact)
async def get_single_artifact(pk: int = Path(..., description='ID of artifact')):
    return await services.ArtifactService.get_object_or_404(pk=pk)


@artifact_router.post('/artifacts', response_model=models.Artifact)
async def create_artifact(schema: schemas.Artifact):
    return await services.ArtifactService.create(schema)


@artifact_router.put('/artifacts/{pk}', response_model=models.Artifact, dependencies=[Security(get_current_superuser)])
async def update_artifact(schema: schemas.Artifact, pk: int = Path(..., description='ID of artifact')):
    return await services.ArtifactService.update(schema, pk=pk)


@artifact_router.delete('/artifacts/{pk}', response_model=models.Artifact, dependencies=[Security(get_current_superuser)])
async def delete_artifact(pk: int = Path(..., description='ID of artifact')):
    return await services.ArtifactService.delete(pk=pk)


@artifact_router.get('/artifact-cores', response_model=models.ArtifactCore)
async def get_artifact_core(artifact_set: int = Query(..., description='ID of artifact set'), artifact_type: ArtifactType = Query(...)):
    return await services.ArtifactCoreService.get_object_or_404(artifact_set=artifact_set, artifact_type=artifact_type)


@artifact_router.post('/artifact-cores', response_model=models.ArtifactCore, dependencies=[Security(get_current_superuser)])
async def create_artifact_core(schema: schemas.ArtifactCoreForm = Depends()):
    return await services.ArtifactCoreService.create(schema)


@artifact_router.get('/artifact-main-stats', response_model=models.ArtifactMainStat)
async def get_artifact_main_stat(
    rarity: int = Query(..., ge=1, le=5),
    level: int = Query(..., ge=0, le=20),
    stat: Stat = Query(...)
):
    return await services.ArtifactMainStatService.get_object_or_404(
        rarity=rarity,
        level=level,
        stat=stat
    )


@artifact_router.get('/{artifact_type}/main-stats', response_model=list[Stat])
async def get_allowed_artifact_main_stats_by_artifact_type(artifact_type: ArtifactType = Path(...)):
    try:
        allowed = ALLOWED_ARTIFACT_MAIN_STATS_FOR_TYPE[artifact_type]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail='Wrong artifact type'
        )
    return allowed


@artifact_router.get('/artifact-sub-stats', response_model=list[models.ArtifactSubStat])
async def get_artifact_sub_stats(
    rarity: int = Query(..., ge=1, le=5),
    stat: Stat = Query(...)
):
    return await services.ArtifactSubStatService.filter(
        rarity=rarity,
        stat=stat
    ).all()


@artifact_router.get('/artifact-sets/{name}', response_model=models.ArtifactSet, dependencies=[Security(get_current_superuser)])
async def get_single_artifact_set(name: str = Path(..., description='Name of artifact set')):
    return await services.ArtifactSetService.get_object_or_404(name=name)


@artifact_router.post('/artifact-sets', response_model=models.ArtifactSet, dependencies=[Security(get_current_superuser)])
async def create_artifact_set(schema: schemas.ArtifactSet):
    return await services.artifact_set_service.create(schema)


@artifact_router.put('/artifact-sets/{pk}', response_model=models.ArtifactSet, dependencies=[Security(get_current_superuser)])
async def update_artifact_set(schema: schemas.ArtifactSet, pk: int = Path(..., description='ID of artifact set')):
    return await services.ArtifactSetService.update(schema, pk=pk)
