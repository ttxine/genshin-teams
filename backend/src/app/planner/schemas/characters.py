from fastapi import Body, File, UploadFile

from src.app.base.services import get_pydantic
from src.app.base.forms import model_form_factory
from src.app.planner.consts import Stat
from src.app.planner.models import characters as models


CharacterCoreFromModel = get_pydantic(models.CharacterCore, 'CharacterCore', exclude={'id', 'image', 'bonus_stat_core', 'characters'})
CharacterLevelMultiplier = get_pydantic(models.CharacterLevelMultiplier, 'CharacterLevelMultiplier', exclude={'id'})
CharacterAscension = get_pydantic(models.CharacterAscension, 'CharacterAscension', exclude={'id'})
CharacterFromModel = get_pydantic(models.Character, 'Character', include={'level', 'ascension'})


class CharacterCore(CharacterCoreFromModel):
    bonus_stat: Stat
    bonus_stat_start_value: int = Body(..., ge=0)
    image: UploadFile = File(...)


CharacterCoreForm = model_form_factory(CharacterCore)


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
    artifact_flower: int = Body(
        ...,
        description='ID of flower',
        gt=0
    )
    artifact_plume: int = Body(
        ...,
        description='ID of plume',
        gt=0
    )
    artifact_sands: int = Body(
        ...,
        description='ID of sands',
        gt=0
    )
    artifact_goblet: int = Body(
        ...,
        description='ID of goblet',
        gt=0
    )
    artifact_circlet: int = Body(
        ...,
        description='ID of circlet',
        gt=0
    )
