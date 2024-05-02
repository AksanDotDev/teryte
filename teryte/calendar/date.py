import enum
import teryte.calendar.enums as _enums
import typing


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


class Strictness(enum.IntEnum):
    ARBITRARY_NO_ERA = 1
    ARBITRARY = 2
    VALID = 3
    CANONICAL = 4


def _check_date_fields(
    era: int, year: int, month: int, day: int,
    strictness: Strictness = Strictness.CANONICAL
):
    if era not in _enums.Era:
        if strictness >= Strictness.VALID:
            raise ValueError(f"Era value '{era}' not recognised in '{_enums.Era}'")
    else:
        era = _enums.Era(era)

    if strictness >= Strictness.ARBITRARY and year < 0:
        raise ValueError("Year value must be greater than 0")

    if strictness >= Strictness.VALID and era > _enums.Era.ZEROTH and (
        era.end is not None and year > era.end.year
    ):
        raise ValueError(f"For Era '{era:s}' year value must less than {era.end.year}")

    if month not in _enums.Month:
        raise ValueError(f"Month value not recognised in {_enums.Month}")
    else:
        month = _enums.Month(month)

    if not 1 <= day <= month.days:
        raise ValueError(f"For Month '{month}' day value must be in 1..{month.days}")

    if strictness == Strictness.CANONICAL:
        if era == _enums.Era.ZEROTH and year == era.end.year and (
            month > era.end.month or month == era.end.month and day < era.end.day
        ):
            raise ValueError(f"For Era '{era:s}' the date must be before {era.end}")

        if era.start is not None and year == era.start.year and (
            month < era.start.month or month == era.start.month and day < era.start.day
        ):
            raise ValueError(f"For Era '{era:s}' the date must be after {era.start}")
        if era.end is not None and year == era.end.year and (
            month > era.end.month or month == era.end.month and day < era.end.day
        ):
            raise ValueError(f"For Era '{era:s}' the date must be before {era.end}")

    return era, year, month, day


class Date:
    """Basic type for Teryte dates.

    Constructors:

    __new__()
    noncanonical()
    arbitrary()
    fromdatestring()
    frominignedate()
    fromordinal()

    Operators:
    __repr__, __str__
    __eq__, __le__, __lt__, __ge__, __gt__, __hash__
    __add__, __radd__, __sub__ (Only with TimeDelta args)

    Methods:

    todatestring()
    toinignedate()
    toordinal()
    ordinalyear()
    month()
    inignemonth()
    weekday()
    inigneweekday()
    canonicaldate()
    yearsinceepoch()
    equivalentdates()
    eraordinalday()

    """

    __slots__ = '_era', '_year', '_month', '_day', '_hashcode'

    def __new__(cls, era: int, year: int, month: int, day: int):
        """Constructor.

        Arguments:

        era, year, month, day (required)
        """
        era, year, month, day = _check_date_fields(era, year, month, day)
        self = object.__new__(cls)
        self._era = era
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        return self

    @classmethod
    def noncanonical(cls, era: int, year: int, month: int, day: int):
        era, year, month, day = _check_date_fields(
            era, year, month, day, Strictness.VALID
        )
        self = object.__new__(cls)
        self._era = era
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        return self

    @classmethod
    def arbitrary(cls, era: typing.Optional[int], year: int, month: int, day: int):
        if era is None:
            era, year, month, day = _check_date_fields(
                era, year, month, day, Strictness.ARBITRARY_NO_ERA
            )
        else:
            era, year, month, day = _check_date_fields(
                era, year, month, day, Strictness.ARBITRARY
            )
        self = object.__new__(cls)
        self._era = era
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        return self

    @classmethod
    def fromdatestring(cls, datestring: str):
        try:
            tokens = datestring.split(".")
            if tokens[0] == "DE":
                if len(tokens) == 4:
                    return cls.arbitrary(None, *map(int, tokens[1:]))
                elif len(tokens) == 2:
                    return cls.fromordinal()
                else:
                    raise ValueError(f'Invalid number of tokens in datestring: {datestring!r}')
            else:
                assert len(tokens) == 4
                return cls.arbitrary(*map(int, tokens))
        except Exception:
            raise ValueError(f'Invalid format datestring: {datestring!r}')

    def todatestring(self):
        return str(self)

    def __str__(self):
        if self.era is not None:
            return f"{self.era:i}.{self.year}.{self.month:i}.{self.day}"
        else:
            return f"DE.{self.year}.{self.month:i}.{self.day}"

    def __repr__(self):
        type_ = type(self)
        return f"<{type_.__module__}.{type_.__qualname__}({self})>"

    def __eq__(self, other):
        if isinstance(other, Date):
            return self._cmp(other) == 0
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Date):
            return self._cmp(other) <= 0
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Date):
            return self._cmp(other) < 0
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Date):
            return self._cmp(other) >= 0
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Date):
            return self._cmp(other) > 0
        else:
            return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, Date)
        s_y, s_m, s_d = self.yearsinceepoch, self.month, self.day
        o_y, o_m, o_d = other.yearsinceepoch, other.month, other.day
        return _cmp((s_y, s_m, s_d), (o_y, o_m, o_d))

    # Read-only field accessors
    @property
    def era(self):
        return self._era

    @property
    def year(self):
        return self._year

    @property
    def yearsinceepoch(self):
        if self.era is None:
            return self.year
        elif self.era is _enums.Era.ZEROTH:
            return -self.year
        elif self.era is _enums.Era.ZEROTH:
            return self.year
        else:
            ordinalyear = self.year
            for i in range(self.era):
                ordinalyear += _enums.Era(i).end.year
            return ordinalyear

    @property
    def month(self):
        return self._month

    @property
    def inignemonth(self):
        return _enums.InigneMonth(self._month)

    @property
    def day(self):
        return self._day

    @property
    def weekday(self):
        wd = self._day % 6
        if wd == 0:
            wd = 6
        return _enums.Day(wd)

    @property
    def inigneweekday(self):
        wd = self._day % 6
        if wd == 0:
            wd = 6
        return _enums.InigneDay(wd)


for i in range(4):
    era = _enums.Era(i)
    if era._start is None:
        era.start = None
    else:
        era.start = Date.arbitrary(i, era._start.year, era._start.month, era._start.day)
    if era._end is None:
        era.end = None
    else:
        era.end = Date.arbitrary(i, era._end.year, era._end.month, era._end.day)
