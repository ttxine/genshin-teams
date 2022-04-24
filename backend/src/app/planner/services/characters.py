from typing import Any

from src.app.base.services import CreateSchema, ModelService, UpdateSchema
from src.app.base.uploads import get_character_upload_path
from src.app.planner.consts import ArtifactType
from src.app.planner.models import characters as models
from src.app.planner.services.artifacts import ArtifactService
from src.app.planner.services.weapons import WeaponService
from src.utils.images import upload_image


class CharacterBonusStatCoreService(ModelService):
    model = models.CharacterBonusStatCore


class CharacterLevelMultiplierService(ModelService):
    model = models.CharacterLevelMultiplier


class CharacterAscensionService(ModelService):
    model = models.CharacterAscension


class CharacterCoreService(ModelService):
    model = models.CharacterCore

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        image = schema.image
        upload_path = get_character_upload_path(schema.name)
        image_path = upload_image(upload_path, image, (250, 250))

        bonus_stat_core = await CharacterBonusStatCoreService.get_or_create(
            stat=schema.bonus_stat,
            start_value=schema.bonus_stat_start_value
        )

        to_save = cls.model.get_pydantic(exclude={'id'})(
            **schema.dict(exclude={'image'}),
            image=image_path,
            bonus_stat_core=bonus_stat_core
        )
        return await super()._pre_save(to_save, exclude_none)


class CharacterService(ModelService):
    model = models.Character

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        character_core = await CharacterCoreService.get_object_or_404(pk=schema.character_core)
        weapon = await WeaponService.get_object_or_404(pk=schema.weapon)

        artifact_flower = await ArtifactService.get_object_or_404(
            pk=schema.artifact_flower,
            core__artifact_type=ArtifactType.FLOWER
        )
        artifact_plume = await ArtifactService.get_object_or_404(
            pk=schema.artifact_plume,
            core__artifact_type=ArtifactType.PLUME_OF_DEATH
        )
        artifact_sands = await ArtifactService.get_object_or_404(
            pk=schema.artifact_sands,
            core__artifact_type=ArtifactType.SANDS_OF_EON
        )
        artifact_goblet = await ArtifactService.get_object_or_404(
            pk=schema.artifact_goblet,
            core__artifact_type=ArtifactType.GOBLET_OF_EONOTHEM
        )
        artifact_circlet = await ArtifactService.get_object_or_404(
            pk=schema.artifact_circlet,
            core__artifact_type=ArtifactType.CIRCLET_OF_LOGOS
        )

        return await super()._pre_save(schema, exclude_none)
