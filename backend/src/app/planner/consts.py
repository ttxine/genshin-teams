from aenum import Enum


class EnumLabelsMixin:

    @property
    def label(self):
        return self.string


class WeaponType(EnumLabelsMixin, Enum):

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


class Stat(EnumLabelsMixin, Enum):
    
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
    # Secondary Stats
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


class DamageType(EnumLabelsMixin, Enum):

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


class StatType(EnumLabelsMixin, Enum):

    _init_ = 'value string'

    CONSTANT = 'const', 'Constant'
    INSTANT = 'inst', 'Instant'
    CONDITIONAL = 'cond', 'Conditional'