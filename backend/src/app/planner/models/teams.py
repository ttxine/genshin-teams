from datetime import datetime

import ormar
from sqlalchemy import func

from src.core.db import BaseMeta
from src.app.user.models import User
from src.app.planner.models.attributes import StatCore
from src.app.planner.models.characters import Character


class ElementalResonanceStat(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'elemental_resonance_stats'

    id: int = ormar.Integer(primary_key=True)


class ElementalResonance(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_resonances'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    effect: ElementalResonanceStat = ormar.ForeignKey(ElementalResonanceStat, unique=True, nullable=False)


class Team(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'teams'

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.Text(max_length=2000)
    author: User = ormar.ForeignKey(User, nullable=False)

    first_character: Character = ormar.ForeignKey(Character, skip_reverse=True, related_name='as_first_in_team', nullable=False)
    second_character: Character = ormar.ForeignKey(Character, skip_reverse=True, related_name='as_second_in_team', nullable=True)
    third_character: Character = ormar.ForeignKey(Character, skip_reverse=True, related_name='as_third_in_team', nullable=True)
    fourth_character: Character = ormar.ForeignKey(Character, skip_reverse=True, related_name='as_fourth_in_team', nullable=True)
    elemental_resonance: ElementalResonance = ormar.ForeignKey(ElementalResonance, nullable=False)

    create_date: datetime = ormar.DateTime(server_default=func.now())
    pub_date: datetime = ormar.DateTime(server_default=func.now())
    public: bool = ormar.Boolean(default=False)


class Vote(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'votes'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    team: Team = ormar.ForeignKey(Team, nullable=False)
