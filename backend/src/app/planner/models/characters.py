import ormar
from src.app.planner.models.weapons import Weapon

from src.core.db import BaseMeta
from src.app.planner.models.artifacts import Artifact
from src.app.planner.consts import Element, WeaponType
from src.app.planner.models.attributes import StatCore


class CharacterBonusStatCore(StatCore):
    class Meta(BaseMeta):
        tablename: str = 'character_bonus_stat_cores'

    id: int = ormar.Integer(primary_key=True)

class CharacterCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'character_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)

    health_start_value: float = ormar.Float(minimum=0)
    attack_start_value: float = ormar.Float(minimum=0)
    deffence_start_value: float = ormar.Float(minimum=0)
    crit_rate_start_value: float = ormar.Float(default=0.05000000074505806)
    crit_damage_start_value: float = ormar.Float(default=0.5)

    bonus_stat_core: CharacterBonusStatCore = ormar.ForeignKey(CharacterBonusStatCore, skip_reverse=True, nullable=False)

    image: str = ormar.String(max_length=255)

    max_ascension_health: float = ormar.Float(minimum=0)
    max_ascension_attack: float = ormar.Float(minimum=0)
    max_ascension_deffence: float = ormar.Float(minimum=0)

    element = ormar.String(max_length=1, choices=list(Element))
    weapon_type = ormar.String(max_length=2, choices=list(WeaponType))


class CharacterLevelMultiplier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'character_level_multipliers'

    id: int = ormar.Integer(primary_key=True)
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    rarity: int = ormar.SmallInteger(minimum=1, maximum=5)
    multiplier: float = ormar.Float(minimum=0)


class CharacterAscension(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'character_ascensions'

    id: int = ormar.Integer(primary_key=True)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6)
    sum_of_sections: int = ormar.SmallInteger(default=38)
    bonus_stat_multiplier: int = ormar.SmallInteger(default=0)


class CharacterBonusStat(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'character_bonus_stats'

    id: int = ormar.Integer(primary_key=True)
    core: CharacterBonusStatCore = ormar.ForeignKey(CharacterBonusStatCore, skip_reverse=True, nullable=False)
    ascension: int = ormar.SmallInteger(minimum=1, maximum=90)
    value: float = ormar.Float(minimum=0)


class Character(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'characters'

    id: int = ormar.Integer(primary_key=True)
    character_core: CharacterCore = ormar.ForeignKey(CharacterCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=1, maximum=90)
    ascension: int = ormar.SmallInteger(minimum=0, maximum=6)
    health: float = ormar.Float(minimum=0)
    attack: float = ormar.Float(minimum=0)
    deffence: float = ormar.Float(minimum=0)
    crit_rate: float = ormar.Float(minimum=0)
    crit_damage: float = ormar.Float(minimum=0)

    elemental_mastery: float = ormar.Float(minimum=0, default=0)
    energy_recharge: float = ormar.Float(minimum=0, default=1)
    healing_bonus: float = ormar.Float(minimum=0, default=0)

    bonus_stat: CharacterBonusStat = ormar.ForeignKey(CharacterBonusStat, nullable=False)

    weapon: Weapon = ormar.ForeignKey(Weapon, nullable=False)

    phys_damage_bonus: float = ormar.Float(minimum=0, default=0)
    anemo_damage_bonus: float = ormar.Float(minimum=0, default=0)
    geo_damage_bonus: float = ormar.Float(minimum=0, default=0)
    electro_damage_bonus: float = ormar.Float(minimum=0, default=0)
    hydro_damage_bonus: float = ormar.Float(minimum=0, default=0)
    pyro_damage_bonus: float = ormar.Float(minimum=0, default=0)
    cryo_damage_bonus: float = ormar.Float(minimum=0, default=0)

    phys_damage_resistance: float = ormar.Float(minimum=0, default=0)
    anemo_damage_resistance: float = ormar.Float(minimum=0, default=0)
    geo_damage_resistance: float = ormar.Float(minimum=0, default=0)
    electro_damage_resistance: float = ormar.Float(minimum=0, default=0)
    hydro_damage_resistance: float = ormar.Float(minimum=0, default=0)
    pyro_damage_resistance: float = ormar.Float(minimum=0, default=0)
    cryo_damage_resistance: float = ormar.Float(minimum=0, default=0)

    stamina: float = ormar.Float(minimum=0, default=100)
    cd_reduction: float = ormar.Float(minimum=0, default=0)
    incoming_healing_bonus: float = ormar.Float(minimum=0, default=0)
    shield_strength: float = ormar.Float(minimum=0, default=0)

    artifact_flower: Artifact = ormar.ForeignKey(Artifact, related_name='characters_as_flower', nullable=False)
    artifact_plume: Artifact = ormar.ForeignKey(Artifact, related_name='characters_as_plume', nullable=False)
    artifact_sands: Artifact = ormar.ForeignKey(Artifact, related_name='characters_as_sands', nullable=False)
    artifact_goblet: Artifact = ormar.ForeignKey(Artifact, related_name='characters_as_goblet', nullable=False)
    artifact_circlet: Artifact = ormar.ForeignKey(Artifact, related_name='characters_as_circlet', nullable=False)

    total_attack: float = ormar.Float(minimum=0)
    total_health: float = ormar.Float(minimum=0)
    total_deffence: float = ormar.Float(minimum=0)
