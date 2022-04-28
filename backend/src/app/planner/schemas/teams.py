from fastapi import Body

from src.app.base.services import get_pydantic
from src.app.planner.models import teams as models
from src.app.planner.schemas.characters import CharacterRelated

TeamFromModel = get_pydantic(models.Team, 'Team', exclude={
    'id',
    'author',
    'first_character',
    'second_character',
    'third_character',
    'fourth_character',
    'elemental_resonance',
    'pub_date',
    'votes'
})
TeamRelatedFromModel = get_pydantic(models.Team, 'Team', exclude={
    'first_character',
    'second_character',
    'third_character',
    'fourth_character',
})


class Team(TeamFromModel):
    first_character: int = Body(..., gt=0, description='ID of character')
    second_character: int = Body(..., gt=0, description='ID of character')
    third_character: int = Body(..., gt=0, description='ID of character')
    fourth_character: int = Body(..., gt=0, description='ID of character')
    elemental_resonance: int = Body(..., gt=0, description='ID of elemental resonance')


class TeamOut(TeamRelatedFromModel):
    first_character: CharacterRelated
    second_character: CharacterRelated
    third_character: CharacterRelated
    fourth_character: CharacterRelated
