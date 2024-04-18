import enum


class PrettyEnumMixin():
    def __format__(self, format_spec: str):
        if format_spec == "i":
            return str(self.value)
        elif format_spec == "":
            return (" ").join(map(str.capitalize, self.name.split("_")))
        else:
            raise ValueError(f"Unknown format code '{format_spec}' for object of type '{type(self)}'")


class ModuloMixin():
    def __add__(self, other: int):
        n = len(type(self))
        x = (int(self) + int(other)) % n
        if x < 1:
            x += n
        return self.__class__(x)

    __radd__ = __add__

    def __sub__(self, other: int):
        n = len(type(self))
        x = (int(self) - int(other)) % n
        if x < 1:
            x += n
        return self.__class__(x)


class MonthMixin():
    @enum.property
    def days(self):
        return self._days

    def __init__(self, value):
        if value == 15:
            self._days = 12
        else:
            self._days = 24
