import enum
import teryte.utils as _utils
from collections import namedtuple


__all__ = ['Day', 'InigneDay', 'Month', 'InigneMonth']


@enum.global_enum
class Day(_utils.PrettyEnumMixin, _utils.ModuloMixin, enum.IntEnum):
    # Standard days of the week
    RESDAY = 1
    FALDAY = 2
    ORDAY = 3
    CONDAY = 4
    EASDAY = 5
    PLADAY = 6


@enum.global_enum
class InigneDay(_utils.PrettyEnumMixin, _utils.ModuloMixin, enum.IntEnum):
    # Inigne days of the week
    RESDAY = 1
    FALDAY = 2
    ORDAY = 3
    CONDAY = 4
    STRADAY = 5
    WORDAY = 6


@enum.global_enum
class Month(_utils.PrettyEnumMixin, _utils.MonthMixin, _utils.ModuloMixin, enum.IntEnum):
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
class InigneMonth(_utils.PrettyEnumMixin, _utils.MonthMixin, _utils.ModuloMixin, enum.IntEnum):
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


# Helper Namedtuple for creating reference eras
# Years are ordinal from 0.0
EraBoundary = namedtuple(
    "EraBoundary",
    [
        "year",
        "month",
        "day"
    ]
)

BOUNDARIES = [
    None,
    EraBoundary(0, 7, 19),
    EraBoundary(720, 10, 21),
    EraBoundary(861, 6, 6),
    None
]

LONG_NAMES = [
    "Before Dragons",
    "Emergence",
    "The Great Crusade",
    "Integration",
]


@enum.global_enum
class Eras(enum.IntEnum):
    # Eras as referencable objects
    ZEROTH = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3

    def __init__(self, value):
        self.short_name = self.name.capitalize()
        self.long_name = LONG_NAMES[value]
        self.start = BOUNDARIES[value]
        self.end = BOUNDARIES[value + 1]
