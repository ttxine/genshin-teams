from fastapi import Body, File, UploadFile
from src.app.base.services import get_pydantic
from src.app.planner.consts import ArtifactType

from src.app.planner.models import artifacts as models
from src.app.base.forms import model_form_factory

ArtifactMainStat = get_pydantic(models.ArtifactMainStat, name='ArtifactMainStat', exclude={'id'})
ArtifactSubStat = get_pydantic(models.ArtifactSubStat, name='ArtifactSubStat', exclude={'id'})
ArtifactSubStatRelated = get_pydantic(models.ArtifactSubStat, name='ArtifactSubStatRelated', exclude={'id', 'rarity'})
ArtifactMainStatRelated = get_pydantic(models.ArtifactMainStat, name='ArtifactMainStatRelated', exclude={'id', 'level', 'rarity'})

ArtifactSetBonus = get_pydantic(models.ArtifactSet, name='ArtifactSetBonusCreate', exclude={'id'})
ArtifactSetFromModel = get_pydantic(
    models.ArtifactSet,
    name='ArtifactSetCreate',
    exclude={'id', 'two_piece_bonus', 'four_piece_bonus'}
)

ArtifactCoreFromModel = get_pydantic(
    models.ArtifactCore,
    name='ArtifactCoreCreate',
    exclude={
        'id',
        'artifact_set',
        'image'
    }
)
ArtifactFromModel = get_pydantic(
    models.ArtifactCore,
    name='Artifact',
    exclude={
        'id',
        'core',
        'main_stat',
        'first_sub_stat',
        'second_sub_stat',
        'third_sub_stat',
        'fourth_sub_stat'
    }
)


class ArtifactCore(ArtifactCoreFromModel):
    artifact_set: int = Body(
        ...,
        description='ID of artifact set',
        gt=0
    )
    image: UploadFile = File(...)


class ArtifactSet(ArtifactSetFromModel):
    two_piece_bonus: ArtifactSetBonus
    four_piece_bonus: ArtifactSetBonus


class Artifact(ArtifactFromModel):
    artifact_set: int = Body(
        ...,
        description='ID of artifact set',
        gt=0
    )
    artifact_type: ArtifactType
    main_stat: ArtifactMainStatRelated
    first_sub_stat: ArtifactSubStatRelated | None
    second_sub_stat: ArtifactSubStatRelated | None
    third_sub_stat: ArtifactSubStatRelated | None
    fourth_sub_stat: ArtifactSubStatRelated | None


ArtifactCoreForm = model_form_factory(ArtifactCore)
