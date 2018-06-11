from enum import Enum


class CardType(Enum):
    ATTACK         = 1
    SKILL          = 2
    POWER          = 3
    STATUS         = 4
    CURSE          = 5


class CardTarget(Enum):
    ENEMY          = 1
    ALL_ENEMY      = 2
    SELF           = 3
    NONE           = 4
    SELF_AND_ENEMY = 5
    ALL            = 6


class CardRarity(Enum):
    BASIC         = 1
    SPECIAL       = 2
    COMMON        = 3
    UNCOMMON      = 4
    RARE          = 5
    CURSE         = 6


class CardColour(Enum):
    RED           = 1
    GREEN         = 2
    BLUE          = 3
    COLOURLESS    = 4
    CURSE         = 5

