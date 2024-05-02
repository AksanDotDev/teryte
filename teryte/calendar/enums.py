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
Epoch = namedtuple(
    "Epoch",
    [
        "year",
        "month",
        "day"
    ]
)

ERA_EPOCHS = [
    (None, Epoch(0, 7, 19)),
    (Epoch(0, 7, 19), Epoch(720, 10, 21)),
    (Epoch(0, 10, 21), Epoch(141, 6, 6)),
    (Epoch(0, 6, 6), None),
]

ERA_LONG_NAMES = [
    "Before Dragons",
    "Emergence",
    "The Great Crusade",
    "Integration",
]


@enum.global_enum
class Era(enum.IntEnum):
    # Eras as referenceable objects
    ZEROTH = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3

    def __init__(self, value):
        self.short_name = self.name.capitalize()
        self.long_name = ERA_LONG_NAMES[value]
        self._start = ERA_EPOCHS[value][0]
        self._end = ERA_EPOCHS[value][1]

    def __format__(self, format_spec: str) -> str:
        if format_spec == "s" or format_spec == "":
            return self.short_name
        elif format_spec == "l":
            return self.long_name
        elif format_spec == "i":
            return str(self.value)
        else:
            raise ValueError(f"Unknown format code '{format_spec}' for object of type '{type(self)}'")

del ERA_EPOCHS
del ERA_LONG_NAMES
