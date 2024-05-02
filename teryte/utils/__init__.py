import enum


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
