class PrettyEnumMixin():
    def __format__(self, _):
        return (" ").join(map(str.capitalize, self.name.split("_")))


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
    def __init__(self, value):
        if value == 15:
            self.days = 12
        else:
            self.days = 24
