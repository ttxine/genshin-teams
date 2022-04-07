import ormar

from src.app.planner.consts import ArtifactType, Rarity
from src.app.planner.models.attributes import StatCore
from src.core.db import BaseMeta


class ArtifactMainStatCore(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'artifact_main_stat_cores'

    id: int = ormar.Integer(primary_key=True)


class ArtifactMainStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_main_stats'

    id: int = ormar.Integer(primary_key=True)
    core: ArtifactMainStatCore = ormar.ForeignKey(ArtifactMainStatCore, skip_reverse=True, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=20)
    value: float = ormar.Float(minimum=0)


class ArtifactSubStatCore(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'artifact_sub_stat_cores'

    id: int = ormar.Integer(primary_key=True)


class ArtifactSubStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_sub_stats'

    id: int = ormar.Integer(primary_key=True)
    core: ArtifactSubStatCore = ormar.ForeignKey(ArtifactSubStatCore, skip_reverse=True, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=20)
    value: float = ormar.Float(minimum=0)


class ArtifactCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Rarity))
    artifact_type: str = ormar.String(max_length=5, choices=list(ArtifactType))
    main_stat_core: ArtifactMainStatCore = ormar.ForeignKey(ArtifactMainStatCore, skip_reverse=True, nullable=False)
    first_sub_stat_core: ArtifactSubStatCore | None = ormar.ForeignKey(ArtifactSubStatCore, skip_reverse=True, related_name='as_first', nullable=True)
    second_sub_stat_core: ArtifactSubStatCore | None = ormar.ForeignKey(ArtifactSubStatCore, skip_reverse=True, related_name='as_second', nullable=True)
    third_sub_stat_core: ArtifactSubStatCore | None = ormar.ForeignKey(ArtifactSubStatCore, skip_reverse=True, related_name='as_third', nullable=True)
    fourth_sub_stat_core: ArtifactSubStatCore | None = ormar.ForeignKey(ArtifactSubStatCore, skip_reverse=True, related_name='as_fourth', nullable=True)


class Artifact(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifacts'

    id: int = ormar.Integer(primary_key=True)
    core: ArtifactCore = ormar.ForeignKey(ArtifactCore, skip_reverse=True, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=20)
    main_stat: ArtifactMainStat = ormar.ForeignKey(ArtifactMainStatCore, skip_reverse=True, nullable=False)
    first_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(ArtifactSubStat, skip_reverse=True, related_name='as_first', nullable=True)
    second_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(ArtifactSubStat, skip_reverse=True, related_name='as_second', nullable=True)
    third_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(ArtifactSubStat, skip_reverse=True, related_name='as_third', nullable=True)
    fourth_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(ArtifactSubStat, skip_reverse=True, related_name='as_fourth', nullable=True)
