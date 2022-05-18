import ormar

from src.core.db import BaseMeta
from src.app.planner.consts import ArtifactType, Stat, StatType


class ArtifactMainStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_main_stats'

    id: int = ormar.Integer(primary_key=True)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    level: int = ormar.SmallInteger(minimum=0, maximum=20)
    stat: str = ormar.String(max_length=10, choices=list(Stat))
    value: float = ormar.Float(minimum=0)


class ArtifactSubStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_sub_stats'

    id: int = ormar.Integer(primary_key=True)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    stat: str = ormar.String(max_length=10, choices=list(Stat))
    value: float = ormar.Float(minimum=0)
    roll: int = ormar.SmallInteger(minimum=1, maximum=6, default=1)


class ArtifactSetBonus(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_set_bonuses'

    id: int = ormar.Integer(primary_key=True)
    stat: str = ormar.String(max_length=10, choices=list(Stat))
    stat_type: str = ormar.String(max_length=5, choices=list(StatType))
    value: float = ormar.Float(minimum=0)
    description: str = ormar.Text()


class ArtifactSet(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_sets'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    max_rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    two_piece_bonus: ArtifactSetBonus = ormar.ForeignKey(
        ArtifactSetBonus,
        skip_reverse=True,
        related_name='as_two_piece',
        nullable=False
    )
    four_piece_bonus: ArtifactSetBonus = ormar.ForeignKey(
        ArtifactSetBonus,
        skip_reverse=True,
        related_name='as_four_piece',
        nullable=False
    )


class ArtifactCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifact_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    artifact_set: ArtifactSet = ormar.ForeignKey(
        ArtifactSet,
        skip_reverse=True,
        nullable=False
    )
    artifact_type: str = ormar.String(max_length=7, choices=list(ArtifactType))
    image: str = ormar.String(max_length=255)


class Artifact(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'artifacts'

    id: int = ormar.Integer(primary_key=True)
    core: ArtifactCore = ormar.ForeignKey(ArtifactCore, skip_reverse=True, nullable=False)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    level: int = ormar.SmallInteger(minimum=0, maximum=20)
    main_stat: ArtifactMainStat = ormar.ForeignKey(
        ArtifactMainStat,
        skip_reverse=True,
        nullable=False
    )
    first_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(
        ArtifactSubStat,
        skip_reverse=True,
        related_name='as_first',
        nullable=True
    )
    second_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(
        ArtifactSubStat,
        skip_reverse=True,
        related_name='as_second',
        nullable=True
    )
    third_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(
        ArtifactSubStat,
        skip_reverse=True,
        related_name='as_third',
        nullable=True
    )
    fourth_sub_stat: ArtifactSubStat | None = ormar.ForeignKey(
        ArtifactSubStat,
        skip_reverse=True,
        related_name='as_fourth',
        nullable=True
    )
