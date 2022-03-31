import ormar

from src.app.planner.consts import Ascension, MultiplierTier, Rarity, Refinement, StatType, WeaponType
from src.app.planner.models.attributes import StatCore
from src.core.db import BaseMeta

# Weapon - Main Stat (Base Attack)
class WeaponMainStatTier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stat_tiers'

    id: int = ormar.Integer(primary_key=True)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Rarity))
    start_value: float = ormar.Float(minimum=0)
    tier: int = ormar.SmallInteger(minimum=1, maximum=4, choices=list(MultiplierTier))


class WeaponMainStatLevelMultiplier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stat_level_multipliers'

    id: int = ormar.Integer(primary_key=True)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Rarity))
    tier: int = ormar.SmallInteger(minimum=1, maximum=4, choices=list(MultiplierTier))
    level: int = ormar.SmallInteger(maximum=90)
    multiplier: float = ormar.Float(minimum=0)


class WeaponMainStatAscensionValue(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_main_stat_ascension_values'

    id: int = ormar.Integer(primary_key=True)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6, choices=list(Ascension))
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Rarity))
    ascension_value: float = ormar.Float(minimum=0)

# Weapon - Sub Stat
class WeaponSubStatLevelMultiplier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_sub_stat_level_multipliers'

    id: int = ormar.Integer(primary_key=True)
    level: int = ormar.SmallInteger(maximum=90)
    multiplier: float = ormar.Float(minimum=0)


class WeaponSubStatCore(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'weapon_sub_stat_cores'

    id: int = ormar.Integer(primary_key=True)


class WeaponSubStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_sub_stats'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponSubStatCore = ormar.ForeignKey(WeaponSubStatCore, skip_reverse=True, nullable=False)
    value: float = ormar.Float(minimum=0)

# Weapon - Passive Ability
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
    passive_ability_core: WeaponPassiveAbilityCore = ormar.ForeignKey(WeaponPassiveAbilityCore, skip_reverse=True, nullable=False)
    stat_type: str = ormar.String(max_length=5, choices=list(StatType))
    max_value: float = ormar.Float(minimum=0)
    refinement_scale: float = ormar.Float(minimum=0)
    position: int = ormar.SmallInteger(minimum=0, default=0)


class WeaponPassiveAbility(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_passive_abilities'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponPassiveAbilityCore = ormar.ForeignKey(WeaponPassiveAbilityCore, skip_reverse=True, nullable=False)
    refinement: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Refinement))
    description: str = ormar.Text()


class WeaponPassiveAbilityStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_passive_ability_stats'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponPassiveAbilityStatCore = ormar.ForeignKey(WeaponPassiveAbilityStatCore, skip_reverse=True, nullable=False)
    refinement: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Refinement))
    value: float = ormar.Float(minimum=0)

    async def get_value_display(self) -> str:
        await self.core.load()
        return '{}%'.format(round(self.value) * 100) if '%' in self.core.stat else str(round(self.value))

# Weapon - Core
class WeaponCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapon_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Rarity))
    main_stat_start_value: float = ormar.Float(minimum=0)
    sub_stat_core: WeaponSubStatCore = ormar.ForeignKey(WeaponSubStatCore, unique=True, skip_reverse=True, nullable=False)
    weapon_type: str = ormar.String(max_length=2, choices=list(WeaponType))
    first_ascension_image: str = ormar.String(max_length=255)
    second_ascension_image: str | None = ormar.String(max_length=255, nullable=True)
    passive_ability_core: WeaponPassiveAbilityCore = ormar.ForeignKey(WeaponPassiveAbilityCore, skip_reverse=True, unique=True, nullable=False)


class Weapon(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'weapons'

    id: int = ormar.Integer(primary_key=True)
    core: WeaponCore = ormar.ForeignKey(WeaponCore, skip_reverse=True, nullable=False)
    level: int = ormar.SmallInteger(maximum=90)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6, choices=list(Ascension))
    main_stat_value: float = ormar.Float(minimum=0)
    sub_stat: WeaponSubStat = ormar.ForeignKey(WeaponSubStat, nullable=False)
    refinement: int = ormar.SmallInteger(minimum=1, maximum=5, choices=list(Refinement))
    passive_ability: WeaponPassiveAbility = ormar.ForeignKey(WeaponPassiveAbility, skip_reverse=True, nullable=False)
