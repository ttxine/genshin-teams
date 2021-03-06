import ormar

from src.core.db import BaseMeta
from src.app.planner.consts import StatType, WeaponType
from src.app.planner.base.models import StatCore


class WeaponMainStatLevelMultiplier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stat_level_multipliers'

    id: int = ormar.Integer(primary_key=True)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    tier: int = ormar.SmallInteger()
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    multiplier: float = ormar.Float(minimum=0)


class WeaponMainStatAscensionValue(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stat_ascension_values'

    id: int = ormar.Integer(primary_key=True)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    ascension_value: float = ormar.Float(minimum=0)


class WeaponMainStatCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stat_cores'

    id: int = ormar.Integer(primary_key=True)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    start_value: float = ormar.Float(minimum=0)
    tier: int = ormar.SmallInteger()
    is_exception: bool = ormar.Boolean(default=False)


class WeaponMainStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stats'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponMainStatCore = ormar.ForeignKey(
        WeaponMainStatCore,
        skip_reverse=True,
        nullable=False
    )
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6)
    value: float = ormar.Float(minimum=0)


class WeaponSubStatLevelMultiplier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_sub_stat_level_multipliers'

    id: int = ormar.Integer(primary_key=True)
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    multiplier: float = ormar.Float(minimum=0)


class WeaponSubStatCore(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'weapon_sub_stat_cores'

    id: int = ormar.Integer(primary_key=True)


class WeaponSubStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_sub_stats'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponSubStatCore = ormar.ForeignKey(
        WeaponSubStatCore,
        skip_reverse=True,
        nullable=False
    )
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    value: float = ormar.Float(minimum=0)


class WeaponPassiveAbilityCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_passive_ability_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    description_template: str = ormar.Text()


class WeaponPassiveAbilityStatCore(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'weapon_passive_ability_stat_cores'

    id: int = ormar.Integer(primary_key=True)
    passive_ability_core: WeaponPassiveAbilityCore = ormar.ForeignKey(
        WeaponPassiveAbilityCore,
        skip_reverse=True,
        nullable=False
    )
    stat_type: str = ormar.String(max_length=5, choices=list(StatType))
    is_special: bool = ormar.Boolean(default=False)
    is_team_buff: bool = ormar.Boolean(default=False)
    max_value: float = ormar.Float(minimum=0)
    refinement_scale: float = ormar.Float(minimum=0)
    position: int = ormar.SmallInteger(minimum=0, default=0)


class WeaponPassiveAbility(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_passive_abilities'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponPassiveAbilityCore = ormar.ForeignKey(
        WeaponPassiveAbilityCore,
        skip_reverse=True,
        nullable=False
    )
    refinement: int = ormar.SmallInteger(minimum=1, maximum=5)
    description: str = ormar.Text()


class WeaponPassiveAbilityStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_passive_ability_stats'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponPassiveAbilityStatCore = ormar.ForeignKey(
        WeaponPassiveAbilityStatCore,
        skip_reverse=True,
        nullable=False
    )
    refinement: int = ormar.SmallInteger(minimum=1, maximum=5)
    value: float = ormar.Float(minimum=0)

    async def get_value_display(self) -> str:
        await self.core.load()
        if '%' in self.core.stat:
            return '{}%'.format(round(self.value * 100))
        return str(round(self.value))


class WeaponCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    main_stat_core: WeaponMainStatCore = ormar.ForeignKey(
        WeaponMainStatCore,
        unique=True,
        skip_reverse=True,
        nullable=False
    )
    sub_stat_core: WeaponSubStatCore = ormar.ForeignKey(
        WeaponSubStatCore,
        unique=True,
        skip_reverse=True,
        nullable=False
    )
    weapon_type: str = ormar.String(max_length=2, choices=list(WeaponType))
    first_ascension_image: str = ormar.String(max_length=255)
    second_ascension_image: str | None = ormar.String(
        max_length=255,
        nullable=True
    )
    passive_ability_core: WeaponPassiveAbilityCore = ormar.ForeignKey(
        WeaponPassiveAbilityCore,
        skip_reverse=True,
        unique=True,
        nullable=False
    )


class Weapon(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapons'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponCore = ormar.ForeignKey(
        WeaponCore,
        skip_reverse=True,
        nullable=False
    )
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6)
    main_stat: WeaponMainStat = ormar.ForeignKey(
        WeaponMainStat,
        skip_reverse=True,
        nullable=False
    )
    sub_stat: WeaponSubStat = ormar.ForeignKey(
        WeaponSubStat,
        skip_reverse=True,
        nullable=False
    )
    refinement: int = ormar.SmallInteger(minimum=1, maximum=5)
    passive_ability: WeaponPassiveAbility = ormar.ForeignKey(
        WeaponPassiveAbility,
        skip_reverse=True,
        nullable=False
    )
