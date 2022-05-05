from src.app.base.services import ModelService, CreateSchema, UpdateSchema
from src.app.planner.models import saved as models


class SavedWeaponService(ModelService):
    model = models.SavedWeapon


class SavedArtifactService(ModelService):
    model = models.SavedArtifact


class SavedCharacterService(ModelService):
    model = models.SavedCharacter
