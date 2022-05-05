from fastapi import Body, File, UploadFile
from pydantic import BaseModel

from src.app.base.services import get_pydantic
from src.app.base.forms import model_form_factory
from src.app.planner.consts import Stat
from src.app.planner.models import characters as models
from src.app.planner.models.artifacts import Artifact


CharacterCoreFromModel = get_pydantic(models.CharacterCore, 'CharacterCore', exclude={'id', 'image', 'bonus_stat_core', 'characters'})
CharacterLevelMultiplier = get_pydantic(models.CharacterLevelMultiplier, 'CharacterLevelMultiplier', exclude={'id'})
CharacterAscension = get_pydantic(models.CharacterAscension, 'CharacterAscension', exclude={'id'})
CharacterFromModel = get_pydantic(models.Character, 'Character', include={'level', 'ascension'})
CharacterBonusStat = get_pydantic(models.CharacterBonusStat, 'CharacterBonusStat')


class CharacterOut(models.Character.get_pydantic()):
    character_core: models.CharacterCore
    artifact_flower: Artifact
    artifact_plume: Artifact
    artifact_sands: Artifact
    artifact_goblet: Artifact
    artifact_circlet: Artifact
    bonus_stat: CharacterBonusStat


class CharacterCore(CharacterCoreFromModel):
    bonus_stat: Stat
    bonus_stat_start_value: float = Body(..., ge=0)
    image: UploadFile = File(...)


CharacterCoreForm = model_form_factory(CharacterCore)


class CharacterRelated(BaseModel):
    character_core: CharacterCore
    level: int
    ascension: int
    health: float
    attack: float
    deffence: float


class Character(CharacterFromModel):
    character_core: int = Body(
        ...,
        description='ID of weapon',
        gt=0
    )
    weapon: int = Body(
        ...,
        description='ID of weapon',
        gt=0
    )
    artifact_flower: int | None = Body(
        None,
        description='ID of flower',
        gt=0
    )
    artifact_plume: int | None = Body(
        None,
        description='ID of plume',
        gt=0
    )
    artifact_sands: int | None = Body(
        None,
        description='ID of sands',
        gt=0
    )
    artifact_goblet: int | None = Body(
        None,
        description='ID of goblet',
        gt=0
    )
    artifact_circlet: int | None = Body(
        None,
        description='ID of circlet',
        gt=0
    )
