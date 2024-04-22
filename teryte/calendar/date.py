import enum
import teryte.calendar.enums as _enums
import typing


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
    __add__, __radd__, __sub__ (Only with timedelta args)

    Methods:

    todatestring()
    toinignedate()
    toordinal()
    weekday()
    inigneweekday()
    month()
    inignemonth()
    canonicaldate()
    eralessdate()
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
            if datestring[0] == 'A':
                tokens = datestring[1:].split(".")
                assert len(tokens) == 3
                return cls.arbitrary(None, *map(int, tokens))
            else:
                tokens = datestring.split(".")
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
            return f"A{self.year}.{self.month:i}.{self.day}"

    def __repr__(self):
        type_ = type(self)
        return f"<{type_.__module__}.{type_.__qualname__}({self})>"

    # Read-only field accessors
    @property
    def era(self):
        return self._era

    @property
    def year(self):
        return self._year

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
