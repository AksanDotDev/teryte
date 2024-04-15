import enum
import teryte.utils as utils


__all__ = ['Day', 'InigneDay', 'Month', 'InigneMonth']


@enum.global_enum
class Day(utils.PrettyEnumMixin, utils.ModuloMixin, enum.IntEnum):
    # Standard days of the week
    RESDAY = 1
    FALDAY = 2
    ORDAY = 3
    CONDAY = 4
    EASDAY = 5
    PLADAY = 6


@enum.global_enum
class InigneDay(utils.PrettyEnumMixin, utils.ModuloMixin, enum.IntEnum):
    # Inigne days of the week
    RESDAY = 1
    FALDAY = 2
    ORDAY = 3
    CONDAY = 4
    STRADAY = 5
    WORDAY = 6


@enum.global_enum
class Month(utils.PrettyEnumMixin, utils.MonthMixin, utils.ModuloMixin, enum.IntEnum):
    # Standard months of the year
    RENEWAL = 1
    FROST_BREAK = 2
    THAW = 3
    BLOSSOM = 4
    GROWTH = 5
    SKYWARD = 6
    HIGH_FLAME = 7
    VERDURE = 8
    REMEMBRANCE = 9
    COMFORT = 10
    GOLD = 11
    EARTHING = 12
    HARVEST = 13
    TWILIGHT = 14
    DEEP_FROST = 15


@enum.global_enum
class InigneMonth(utils.PrettyEnumMixin, utils.MonthMixin, utils.ModuloMixin, enum.IntEnum):
    # Inigne months of the year
    RENEWAL = 1
    FROST_BREAK = 2
    THAW = 3
    BLOSSOM = 4
    GROWTH = 5
    SKYWARD = 6
    HIGH_SUMMER = 7
    VERDURE = 8
    REMEMBRANCE = 9
    COMFORT = 10
    GOLD = 11
    EARTHING = 12
    HARVEST = 13
    TWILIGHT = 14
    DEEP_FROST = 15
