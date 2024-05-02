import enum
import teryte.calendar.enums as _enums
import typing as T


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


class Strictness(enum.IntEnum):
    ARBITRARY_NO_ERA = 1
    ARBITRARY = 2
    VALID = 3
    CANONICAL = 4


def _check_date_fields(
    year: int, month: int, day: int
):
    if month not in _enums.Month:
        raise ValueError(f"Month value not recognised in {_enums.Month}")

    e_month = _enums.Month(month)
    if not 1 <= day <= e_month.days:
        raise ValueError(f"For Month '{e_month}' day value must be in 1..{e_month.days}")

    return year, month, day


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
    erayear()
    equivalentdates()
    eraordinalday()

    """

    __slots__ = '_year', '_month', '_day', '_hashcode'
    _year: int
    _month: int
    _day: int
    _hashcode: int

    def __new__(cls, year: int, month: int, day: int) -> T.Self:
        """Constructor.

        Arguments:

        year, month, day (required)
        """
        year, month, day = _check_date_fields(year, month, day)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hashcode = -1
        return self

    @classmethod
    def fromdatestring(cls, datestring: str) -> T.Self:
        try:
            pass
        except Exception:
            raise ValueError(f'Invalid format datestring: {datestring!r}')

    def todatestring(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.era is not None:
            return f"{self.era:i}.{self.year}.{self.month:i}.{self.day}"
        else:
            return f"DE.{self.year}.{self.month:i}.{self.day}"

    def __repr__(self) -> str:
        type_ = type(self)
        return f"<{type_.__module__}.{type_.__qualname__}({self})>"

    def __eq__(self, other) -> bool:
        if isinstance(other, Date):
            return self._cmp(other) == 0
        else:
            return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, Date):
            return self._cmp(other) <= 0
        else:
            return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, Date):
            return self._cmp(other) < 0
        else:
            return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, Date):
            return self._cmp(other) >= 0
        else:
            return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, Date):
            return self._cmp(other) > 0
        else:
            return NotImplemented

    def _cmp(self, other: T.Self) -> T.Literal[-1, 0, 1]:
        assert isinstance(other, Date)
        return _cmp(self._getstate(), other._getstate())

    def __hash__(self) -> int:
        "Hash."
        if self._hashcode == -1:
            yhi, ylo = divmod(self._year, 256)
            self._hashcode = hash(bytes([yhi, ylo, self._month, self._day]))
        return self._hashcode

    # Read-only field accessors
    @property
    def era(self) -> _enums.Era:
        pass

    @property
    def year(self) -> int:
        return self._year

    @property
    def erayear(self) -> int:
        pass

    @property
    def month(self) -> _enums.Month:
        return _enums.Month(self._month)

    @property
    def inignemonth(self) -> _enums.InigneMonth:
        return _enums.InigneMonth(self._month)

    @property
    def day(self) -> int:
        return self._day

    @property
    def weekday(self) -> _enums.Day:
        wd = self._day % 6
        if wd == 0:
            wd = 6
        return _enums.Day(wd)

    @property
    def inigneweekday(self) -> _enums.InigneDay:
        wd = self._day % 6
        if wd == 0:
            wd = 6
        return _enums.InigneDay(wd)

    def _getstate(self) -> T.Tuple[int, int, int]:
        return (self._year, self._month, self._day)

    __getnewargs__ = _getstate


for era in _enums.Era:
    if era._start is None:
        era.start = None  # type: ignore[attr-defined]
    else:
        era.start = Date(era._start.year, era._start.month, era._start.day)  # type: ignore[attr-defined]
    if era._end is None:
        era.end = None  # type: ignore[attr-defined]
    else:
        era.end = Date(era._end.year, era._end.month, era._end.day)  # type: ignore[attr-defined]
