from fastapi import Body

from src.app.planner.models import artifacts as models


ArtifactMainStatCore = models.ArtifactMainStatCore.get_pydantic(exclude={'id'})
ArtifactSubStatCore = models.ArtifactSubStatCore.get_pydantic(exclude={'id'})

ArtifactMainStatFromModel = models.ArtifactMainStat.get_pydantic(exclude={'id', 'core'})
ArtifactSubStatFromModel = models.ArtifactSubStat.get_pydantic(exclude={'id', 'core'})

ArtifactCore = models.ArtifactCore.get_pydantic(exclude={'id'})

ArtifactFromModel = models.Artifact.get_pydantic(exclude={
    'id',
    'core',
    'main_stat',
    'first_sub_stat',
    'second_sub_stat',
    'third_sub_stat',
    'fourth_sub_stat'
})


class ArtifactMainStatCU(ArtifactMainStatFromModel):
    core: int = Body(
        ...,
        description='ID of artifact main stat core',
        gt=0
    )


class ArtifactSubStatCU(ArtifactSubStatFromModel):
    core: int = Body(
        ...,
        description='ID of artifact sub stat core',
        gt=0
    )


class ArtifactCU(ArtifactFromModel):
    core: int = Body(
        ...,
        description='ID of artifact core',
        gt=0
    )
