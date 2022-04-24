import ormar

from src.app.planner.consts import PassiveTalentType, Stat
from src.app.planner.models.characters import CharacterCore
from src.core.db import BaseMeta


class TalentLevelMultiplierType(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'talant_level_multiplier_types'

    id: int = ormar.Integer(primary_key=True)
    name = ormar.String(max_length=100, nullable=False)


class TalentLevelMultiplier(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'talant_level_multipliers'

    id: int = ormar.Integer(primary_key=True)
    multiplier_type: TalentLevelMultiplierType = ormar.ForeignKey(TalentLevelMultiplierType, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)
    multiplier = ormar.Float(minimum=0)

# NORMAL ATTACK TALENT
class NormalAttackTalentCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'normal_attack_talant_cores'

    id: int = ormar.Integer(primary_key=True)
    name = ormar.String(max_length=100, nullable=False)
    character_core: CharacterCore = ormar.ForeignKey(CharacterCore, unique=True, nullable=False)

class NormalAttackTalent(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'normal_attack_talants'

    id: int = ormar.Integer(primary_key=True)
    core: NormalAttackTalentCore = ormar.ForeignKey(NormalAttackTalentCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)


class NormalAttackCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'normal_attack_cores'

    id: int = ormar.Integer(primary_key=True)
    talent_core: NormalAttackTalentCore = ormar.ForeignKey(NormalAttackTalentCore, unique=True, nullable=False)

    multiplier_type: TalentLevelMultiplierType = ormar.ForeignKey(TalentLevelMultiplierType, nullable=False)

    first_hit_damage_start_value: float = ormar.Float(minimum=0)
    second_hit_damage_start_value: float | None = ormar.Float(minimum=0, nullable=True)
    third_hit_damage_start_value: float | None = ormar.Float(minimum=0, nullable=True)
    fourth_hit_damage_start_value: float | None = ormar.Float(minimum=0, nullable=True)
    fifth_hit_damage_start_value: float | None = ormar.Float(minimum=0, nullable=True)
    sixth_hit_damage_start_value: float | None = ormar.Float(minimum=0, nullable=True)

    description: str = ormar.Text(max_length=2000)


class NormalAttack(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'normal_attacks'

    id: int = ormar.Integer(primary_key=True)
    core: NormalAttackCore = ormar.ForeignKey(NormalAttackCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)

    first_hit_damage: float = ormar.Float(minimum=0)
    second_hit_damage: float | None = ormar.Float(minimum=0, nullable=True)
    third_hit_damage: float | None = ormar.Float(minimum=0, nullable=True)
    fourth_hit_damage: float | None = ormar.Float(minimum=0, nullable=True)
    fifth_hit_damage: float | None = ormar.Float(minimum=0, nullable=True)
    sixth_hit_damage: float | None = ormar.Float(minimum=0, nullable=True)


class PlungingAttackCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'plunging_attack_cores'

    id: int = ormar.Integer(primary_key=True)
    normal_attack_talent_core: NormalAttackTalentCore = ormar.ForeignKey(NormalAttackTalentCore, unique=True, nullable=False)
    multiplier_type: TalentLevelMultiplierType = ormar.ForeignKey(TalentLevelMultiplierType, nullable=False)

    plunge_damage_start_value: float = ormar.Float(minimum=0)
    low_plunge_damage_start_value: float = ormar.Float(minimum=0)
    high_plunge_damage_start_value: float = ormar.Float(minimum=0)

    description: str = ormar.Text(max_length=2000)


class PlungingAttack(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'plunging_attacks'

    id: int = ormar.Integer(primary_key=True)
    core: PlungingAttackCore = ormar.ForeignKey(PlungingAttackCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)

    plunge_damage: float = ormar.Float(minimum=0)
    low_plunge_damage: float = ormar.Float(minimum=0)
    high_plunge_damage: float = ormar.Float(minimum=0)


class ChargedAttackCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'charged_attack_cores'

    id: int = ormar.Integer(primary_key=True)
    normal_attack_talent_core: NormalAttackTalentCore = ormar.ForeignKey(NormalAttackTalentCore, unique=True, nullable=False)
    multiplier_type: TalentLevelMultiplierType = ormar.ForeignKey(TalentLevelMultiplierType, nullable=False)
    stamina: float = ormar.Float(minimum=0)
    description: str = ormar.Text(max_length=2000)


class ChargedAttack(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'charged_attacks'

    id: int = ormar.Integer(primary_key=True)
    core: ChargedAttackCore = ormar.ForeignKey(ChargedAttackCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)


class ChargedAttackDamageCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'charged_attack_damage_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    charged_attack_core: ChargedAttackCore = ormar.ForeignKey(ChargedAttackCore, nullable=False)
    start_value: float = ormar.Float(minimum=0)
    is_elemental: bool = ormar.Boolean(default=False, nullable=False)


class ChargedAttackDamage(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'charged_attack_damages'

    id: int = ormar.Integer(primary_key=True)
    charged_attack_damage_core: ChargedAttackDamageCore = ormar.ForeignKey(ChargedAttackDamageCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)
    value: float = ormar.Float(minimum=0)

# ELEMENTAL SKILL TALENT
class ElemetalSkillTalentCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_skill_talent_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    character_core: CharacterCore = ormar.ForeignKey(CharacterCore, unique=True, nullable=False)
    description: str = ormar.Text(max_length=2000)
    multiplier_type: TalentLevelMultiplierType = ormar.ForeignKey(TalentLevelMultiplierType, nullable=False)


class ElementalSkillTalentAttributeCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_skill_talent_attribute_cores'

    id: int = ormar.Integer(primary_key=True)
    elemental_skill_talent_core: ElemetalSkillTalentCore = ormar.ForeignKey(ElemetalSkillTalentCore, nullable=False)
    name: str = ormar.String(max_length=100)
    base_value: float = ormar.Float(minimum=0)
    is_elemental: bool = ormar.Boolean(default=False, nullable=False)


class ElementalSkillTalent(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_skill_talents'

    id: int = ormar.Integer(primary_key=True)
    core: ElemetalSkillTalentCore = ormar.ForeignKey(ElemetalSkillTalentCore, nullable=False)
    level: int = ormar.SmallInteger(minimum=0, maximum=15)


class ElementalSkillAttribute(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_skill_attributes'

    id: int = ormar.Integer(primary_key=True)
    elemental_skill_talent: ElementalSkillTalent = ormar.ForeignKey(ElementalSkillTalent, nullable=False)
    value: float = ormar.Float(minimum=0)

# ELEMENTAL BURST TALENT
class ElementalBurstTalentCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_burst_talent_cores'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    character_core: CharacterCore = ormar.ForeignKey(CharacterCore, unique=True, nullable=False)
    description: str = ormar.Text(max_length=2000)
    multiplier_type: TalentLevelMultiplierType = ormar.ForeignKey(TalentLevelMultiplierType, nullable=False)


class ElementalBurstTalentAttributeCore(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_burst_talent_attribute_cores'

    id: int = ormar.Integer(primary_key=True)
    elemental_burst_talent_core: ElementalBurstTalentCore = ormar.ForeignKey(ElementalBurstTalentCore, nullable=False)
    name: str = ormar.String(max_length=100)
    base_value: float = ormar.Float(minimum=0)
    is_elemental: bool = ormar.Boolean(default=False, nullable=False)


class ElementalBurstTalent(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_burst_talents'

    id: int = ormar.Integer(primary_key=True)
    core: ElementalBurstTalentCore = ormar.ForeignKey(ElementalBurstTalentCore, nullable=False)
    value: float = ormar.Float(minimum=0)


class ElementalBurstAttribute(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'elemental_burst_attributes'

    id: int = ormar.Integer(primary_key=True)
    elemental_burst_talent: ElementalBurstTalent = ormar.ForeignKey(ElementalBurstTalent, nullable=False)
    value: float = ormar.Float(minimum=0)


class PassiveTalentAttribute(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'passive_talent_attributes'

    id: int = ormar.Integer(primary_key=True)
    stat: str = ormar.String(max_length=10, choices=list(Stat))
    value: float = ormar.Float(minimum=0)


class PassiveTalent(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'passive_talents'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    character_core: CharacterCore = ormar.ForeignKey(CharacterCore, unique=True, nullable=False)
    description: str = ormar.Text(max_length=2000)
    passive_talent_type = ormar.String(max_length=3, choices=list(PassiveTalentType))
    attribute: PassiveTalentAttribute = ormar.ForeignKey(PassiveTalentAttribute, unique=True, nullable=False)
