from aenum import Enum, StrEnum


ALLOWED_ARTIFACT_MAIN_STATS_FOR_TYPE = {
    'flower': ('hp',),
    'plume': ('atk',),
    'sands': ('hp%', 'atk%', 'def%', 'em', 'er%'),
    'goblet': ('hp%', 'atk%', 'def%', 'em', 'elem%', 'phys%'),
    'circlet': ('hp%', 'atk%', 'def%', 'em', 'cr%', 'cd%', 'heal%')
}


class EnumLabelsMixin:

    @property
    def label(self):
        return self.string


class WeaponType(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    SWORDS = 'sw', 'Swords'
    CLAYMORES = 'cl', 'Claymores'
    POLEARMS = 'po', 'Polearms'
    CATALYSTS = 'ca', 'Catalysts'
    BOWS = 'bo', 'Bows'


class Rarity(EnumLabelsMixin, Enum):

    _init_ = 'value string'

    ONE = 1, '★'
    TWO = 2, '★★'
    THREE = 3, '★★★'
    FOUR = 4, '★★★★'
    FIVE = 5, '★★★★★'


class Ascension(EnumLabelsMixin, Enum):

    _init_ = 'value string'

    NULL = 0, 'Non-Ascended'
    FIRST = 1, '1st Ascension'
    SECOND = 2, '2nd Ascension'
    THIRD = 3, '3rd Ascension'
    FOURTH = 4, '4th Ascension'
    FIFTH = 5, '5th Ascension'
    SIXTH = 6, '6th Ascension'


class Refinement(EnumLabelsMixin, Enum):

    _init_ = 'value string'

    FIRST = 1, '1st Refinement'
    SECOND = 2, '2nd Refinement'
    THIRD = 3, '3rd Refinement'
    FOURTH = 4, '4th Refinement'
    FIFTH = 5, '5th Refinement'


class Stat(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    HP = 'hp', 'HP'
    HP_PERCENT = 'hp%', 'HP%'
    ATK = 'atk', 'ATK'
    ATK_PERCENT = 'atk%', 'ATK%'
    DEF = 'def', 'DEF'
    DEF_PERCENT = 'def%', 'DEF%'
    ELEMENTAL_MASTERY = 'em', 'Elemental Mastery'
    ENERGY_RECHARGE = 'er%', 'Energy Recharge%'
    HEAL_BONUS = 'heal%', 'Healing Bonus%'
    CRIT_RATE = 'cr%', 'Crit Rate%'
    CRIT_DMG = 'cd%', 'Crit DMG%'

    ELEMENTAL_DMG_BONUS = 'elem%', 'Elemental DMG Bonus%'
    PHYS_DMG_BONUS = 'phys%', 'Physical DMG Bonus%'
    ANEMO_DMG_BONUS = 'anemo%', 'Anemo DMG Bonus%'
    GEO_DMG_BONUS = 'geo%', 'Geo DMG Bonus%'
    ELECTRO_DMG_BONUS = 'electro%', 'Electro DMG Bonus%'
    HYDRO_DMG_BONUS = 'hydro%', 'Hydro DMG Bonus%'
    PYRO_DMG_BONUS = 'pyro%', 'Pyro DMG Bonus%'
    CRYO_DMG_BONUS = 'cryo%', 'Hydro DMG Bonus%'
    PHYS_DMG_RES = 'physr%', 'Physical DMG RES%'
    ANEMO_DMG_RES = 'anemor%', 'Anemo DMG RES%'
    GEO_DMG_RES = 'geor%', 'Geo DMG RES%'
    ELECTRO_DMG_RES = 'electror%', 'Electro DMG RES%'
    HYDRO_DMG_RES = 'hydror%', 'Hydro DMG RES%'
    PYRO_DMG_RES = 'pyror%', 'Pyro DMG RES%'
    CRYO_DMG_RES = 'cryor%', 'Hydro DMG RES%'
    STAMINA = 'stamina', 'Stamina'
    CD_REDUCTION = 'cdr%', 'CD Reduction'
    INCOMING_HEAL_BONUS = 'iheal%', 'Incoming Healing Bonus'
    SHIELD_STRENGTH = 'shield%', 'Shield Strength'
    HEAL = 'heal%', 'Heal'

    COMMON_DMG_BONUS = 'common%', 'Common DMG Bonus'
    ENEMY_PHYSICAL_DMG_RES = 'ephysr%'
    ENEMY_ANEMO_DMG_RES = 'enemor%', 'Anemo DMG RES%'
    ENEMY_GEO_DMG_RES = 'egeor%', 'Geo DMG RES%'
    ENEMY_ELECTRO_DMG_RES = 'eelectror%', 'Electro DMG RES%'
    ENEMY_HYDRO_DMG_RES = 'ehydror%', 'Hydro DMG RES%'
    ENEMY_PYRO_DMG_RES = 'epyror%', 'Pyro DMG RES%'
    ENEMY_CRYO_DMG_RES = 'ecryor%', 'Hydro DMG RES%'
    NORMAL_ATK_DMG_BONUS = 'norm%'
    NORMAL_ATK_CRIT_RATE_BONUS = 'normcr%'
    CHARGED_ATK_DMG_BONUS = 'char%'
    CHARGED_ATK_CRIT_RATE_BONUS = 'charcr%'
    PLUNGING_ATK_DMG_BONUS = 'plan%'
    PLUNGING_ATK_CRIT_RATE_BONUS = 'plancr%'
    ELEMENTAL_SKILL_DMG_BONUS = 'elemsk%'
    ELEMENTAL_SKILL_CRIT_RATE_BONUS = 'elemskcr%'
    ELEMENTAL_BURST_DMG_BONUS = 'elembu%'
    ELEMENTAL_BURST_CRIT_RATE_BONUS = 'elembucr%'
    OVERLOADED_DMG_BONUS = 'over%'
    SHATTERED_DMG_BONUS = 'shat%'
    ELECTRO_CHARGED_DMG_BONUS = 'elchover%'
    SUPERCONDUCT_DMG_BONUS = 'sucond%'
    SWIRL_DMG_BONUS = 'swirl%'
    VAPORIZE_DMG_BONUS = 'vapo%'
    MELT_DMG_BONUS = 'melt%'
    MOVEMENT_SPEED = 'ms%'
    ATTACK_SPEED = 'ms%'
    WEAKSPOT_DMG = 'weak%'
    DMG_REDUCTION = 'dmgr%'


class DamageType(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    PHYS = 'phys', 'Physical'
    ANEMO = 'anemo', 'Anemo'
    GEO = 'geo', 'Geo'
    ELECTRO = 'electro', 'Electro'
    HYDRO = 'hydro', 'Hydro'
    PYRO = 'pyro', 'Pyro'
    CRYO = 'cryo', 'Cryo'


class MultiplierTier(EnumLabelsMixin, Enum):

    _init_ = 'value string'

    FIRST_TIER = 1, 'Tier 1'
    SECOND_TIER = 2, 'Tier 2'
    THIRD_TIER = 3, 'Tier 3'
    FOURTH_TIER = 4, 'Tier 4'


class StatType(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    CONSTANT = 'const', 'Constant'
    INSTANT = 'inst', 'Instant'
    CONDITIONAL = 'cond', 'Conditional'


class ArtifactType(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    FLOWER = 'flower', 'Flower of Life'
    PLUME_OF_DEATH = 'plume', 'Plume of Death'
    SANDS_OF_EON = 'sands', 'Sands of Eon'
    GOBLET_OF_EONOTHEM = 'goblet', ' Goblet of Eonothem'
    CIRCLET_OF_LOGOS = 'circlet', 'Circlet of Logos'


class PassiveTalentType(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    FIRST_ASCENSION_PASSIVE = '1ap', 'First Ascension Passive'
    FOURTH_ASCENSION_PASSIVE = '4ap', 'Fourth Ascension Passive'
    UTILITY_PASSIVE = 'up', 'Utility Passive'


class Element(EnumLabelsMixin, StrEnum):

    _init_ = 'value string'

    PYRO = 'p', 'Pyro'
    HYDRO = 'h', 'Hydro'
    ANEMO = 'a', 'Anemo'
    ELECTRO = 'e', 'Electro'
    CRYO = 'c', 'Cryo'
    GEO = 'g', 'Geo'
