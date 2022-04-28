from typing import Type, Any
from fastapi import HTTPException

from ormar import Model

from src.app.base.services import ModelService, CreateSchema, UpdateSchema
from src.app.base.uploads import get_artifact_upload_path
from src.app.planner.consts import ALLOWED_ARTIFACT_MAIN_STATS_FOR_TYPE
from src.app.planner.models import artifacts as models
from src.utils.images import upload_image


class ArtifactSubStatService(ModelService):
    model: Type[Model] = models.ArtifactSubStat


class ArtifactMainStatService(ModelService):
    model: Type[Model] = models.ArtifactMainStat


class ArtifactSetBonusService(ModelService):
    model: Type[Model] = models.ArtifactSetBonus


class ArtifactSetService(ModelService):
    model: Type[Model] = models.ArtifactSet

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        bonus_service = ArtifactSetBonusService()
        two_piece_bonus = await bonus_service.get_or_create(schema.two_piece_bonus)
        four_piece_bonus = await bonus_service.get_or_create(schema.four_piece_bonus)

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={
                'two_piece_bonus',
                'four_piece_bonus'
            }),
            two_piece_bonus=two_piece_bonus,
            four_piece_bonus=four_piece_bonus
        )

        return await super()._pre_save(to_save, exclude_none)


class ArtifactCoreService(ModelService):
    model: Type[Model] = models.ArtifactCore

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        artifact_set = await ArtifactSetService().get_object_or_404(
            pk=schema.artifact_set
        )

        upload_path = get_artifact_upload_path(schema.name)
        image_path = upload_image(upload_path, schema.image, (250, 250))

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={
                'artifact_set',
                'image'
            }),
            artifact_set=artifact_set,
            image=image_path
        )

        return await super()._pre_save(to_save, exclude_none)


class ArtifactService(ModelService):
    model: Type[Model] = models.Artifact

    @classmethod
    async def _pre_save(cls, schema: CreateSchema | UpdateSchema, exclude_none: bool = True) -> dict[str, Any]:
        artifact_set = await ArtifactSetService().get_object_or_404(
            pk=schema.artifact_set
        )

        if schema.main_stat.stat not in ALLOWED_ARTIFACT_MAIN_STATS_FOR_TYPE[schema.artifact_type]:
            raise HTTPException(
                status_code=400,
                detail='Wrong main stat'
            )

        max_rarity = artifact_set.max_rarity
        rarity = schema.rarity

        if (max_rarity == 3 and rarity > 3 or 
                max_rarity > 4 and max_rarity - rarity > 1):
            raise HTTPException(
                status_code=400,
                detail='Wrong rarity'
            )

        core = await ArtifactCoreService().get_object_or_404(
            artifact_set=schema.artifact_set,
            artifact_type=schema.artifact_type
        )

        main_stat = await ArtifactMainStatService().get_object_or_404(
            **schema.main_stat.dict(),
            rarity=schema.rarity,
            level=schema.level
        )

        if schema.first_sub_stat:
            first_sub_stat = await ArtifactSubStatService().get_object_or_404(
                **schema.first_sub_stat.dict(), rarity=schema.rarity
            )
        else:
            first_sub_stat = None

        if schema.second_sub_stat:
            second_sub_stat = await ArtifactSubStatService().get_object_or_404(
                **schema.second_sub_stat.dict(), rarity=schema.rarity
            )
        else:
            second_sub_stat = None

        if schema.third_sub_stat:
            third_sub_stat = await ArtifactSubStatService().get_object_or_404(
                **schema.third_sub_stat.dict(), rarity=schema.rarity
            )
        else:
            third_sub_stat = None

        if schema.fourth_sub_stat:
            fourth_sub_stat = await ArtifactSubStatService().get_object_or_404(
                **schema.first_sub_stat.dict(), rarity=schema.rarity
            )
        else:
            fourth_sub_stat = None

        ModelSchema = cls.model.get_pydantic(exclude={'id'})
        to_save = ModelSchema(
            **schema.dict(exclude={
                'core',
                'main_stat',
                'first_sub_stat',
                'second_sub_stat',
                'third_sub_stat',
                'fourth_sub_stat'
            }),
            core=core,
            main_stat=main_stat,
            first_sub_stat=first_sub_stat,
            second_sub_stat=second_sub_stat,
            third_sub_stat=third_sub_stat,
            fourth_sub_stat=fourth_sub_stat,
        )

        return await super()._pre_save(to_save, exclude_none)


artifact_sub_stat_service = ArtifactSubStatService()
artifact_main_stat_service = ArtifactMainStatService()
artifact_set_bonus_service = ArtifactSetBonusService()
artifact_set_service = ArtifactSetService()
artifact_core_service = ArtifactCoreService()
artifact_service = ArtifactService()
