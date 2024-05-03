import enum
import typing as T


class DataIntEnum(enum.IntEnum):
    def __new__(cls, value, *args) -> T.Self:
        obj = int.__new__(cls)
        obj._value_ = value
        return obj


class DataEnum(enum.Enum):
    def __new__(cls, *args) -> T.Self:
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class PrettyEnumMixin():
    value: int
    name: str

    def __format__(self, format_spec: str) -> str:
        if format_spec == "i":
            return str(self.value)
        elif format_spec == "":
            return (" ").join(map(str.capitalize, self.name.split("_")))
        else:
            raise ValueError(f"Unknown format code '{format_spec}' for object of type '{type(self)}'")


class MonthMixin():
    @enum.property
    def days(self) -> int:
        return self._days

    def __init__(self, value: int):
        if value == 15:
            self._days = 12
        else:
            self._days = 24
