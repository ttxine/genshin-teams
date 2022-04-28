import ormar

from src.core.db import BaseMeta
from src.app.user.models import User
from src.app.planner.models.weapons import Weapon
from src.app.planner.models.artifacts import Artifact
from src.app.planner.models.characters import Character


class SavedWeapon(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'saved_weapons'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, skip_reverse=True, nullable=False)
    weapon: Weapon = ormar.ForeignKey(Weapon, skip_reverse=True, nullable=False)


class SavedArtifact(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'saved_artifacts'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, skip_reverse=True, nullable=False)
    artifact: Artifact = ormar.ForeignKey(Artifact, skip_reverse=True, nullable=False)


class SavedCharacter(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'saved_characters'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, skip_reverse=True, nullable=False)
    character: Character = ormar.ForeignKey(Character, skip_reverse=True, nullable=False)
