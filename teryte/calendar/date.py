import typing as T
import enum
import teryte.utils as _utils

_DAYS_IN_YEAR = 348
_DAYS_IN_STANDARD_MONTH = 24


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def _check_date_fields(
    year: int, month: int, day: int
) -> tuple[int, int, int]:
    assert isinstance(year, int)
    if month not in Month:
        raise ValueError(f"Month value not recognised in {Month}")

    e_month = Month(month)
    if not 1 <= day <= e_month.days:
        raise ValueError(f"For Month '{e_month}' day value must be in 1..{e_month.days}")

    return year, month, day


def _unify_era_date(
    era: int, year: int, month: int, day: int
) -> tuple[int, int, int]:
    if era not in Era:
        raise ValueError(f"Era value '{era}' not recognised in '{Era}'")
    if year < 0:
        raise ValueError(f"Year value '{year}' invalid, era years must be >= 0")
    e_era = Era(era)
    if e_era.negated:
        year = -year
    if e_era.start is not None:
        year += e_era.start.year
        if (year, month, day) < e_era.start._getstate():
            raise ValueError(f"For Era '{e_era:s}' the date must be after {e_era.start:c}")
    if e_era.end is not None and (year, month, day) > e_era.end._getstate():
        raise ValueError(f"For Era '{e_era:s}' the date must be before {e_era.end:c}")
    return year, month, day


def _unify_ordinal_date(
    day: int, calendar: 'ReferenceCalendars'
) -> tuple[int, int, int]:
    if day < 0:
        raise ValueError(f"Day value '{day}' invalid, ordinal days must be >= 0")
    if calendar.max is not None and day > calendar.max:
        raise ValueError(f"For Calendar '{calendar:s}' the day value '{day}' must be <= {calendar.max}")
    if calendar.negated:
        temp = calendar.epoch - DateDelta(days=day)
    else:
        temp = calendar.epoch + DateDelta(days=day)
    return temp._year, temp._month, temp._day


def _reconcile_date_arithmatic(
    date: tuple[int, int, int],
    delta: tuple[int, int]
):
    year, month, day = date
    d_year, d_day = delta
    year += d_year
    day += d_day
    e_month = Month(month)
    while day < 0:
        year -= 1
        day += _DAYS_IN_YEAR
    while day > e_month.days:
        if month == 15:
            month = 1
            day -= e_month.days
            year += 1
        else:
            month += 1
            day -= e_month.days
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
    __repr__, __str__, __format__
    __eq__, __le__, __lt__, __ge__, __gt__, __hash__
    __add__, __radd__, __sub__

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
            tokens = datestring.split(".")
            if len(tokens) == 4:
                month = int(tokens[2])
                day = int(tokens[3])
                if tokens[0] == "BDE":
                    year = -int(tokens[1])
                elif tokens[0] == "ADE":
                    year = int(tokens[1])
                else:
                    era = int(tokens[0])
                    year = int(tokens[1])
                    year, month, day = _unify_era_date(era, year, month, day)
            elif len(tokens) == 2:
                raise NotImplementedError()
            else:
                raise ValueError(f'Invalid number of tokens in datestring: {datestring!r}')
            year, month, day = _check_date_fields(year, month, day)
            self = object.__new__(cls)
            self._year = year
            self._month = month
            self._day = day
            self._hashcode = -1
            return self
        except Exception:
            raise ValueError(f'Invalid format datestring: {datestring!r}')

    def todatestring(self) -> str:
        # TODO make more akin to the OG date function.
        return format(self, "canonical")

    def replace(
        self,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None
    ) -> T.Self:
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        return type(self)(year, month, day)

    def __str__(self) -> str:
        return format(self, "eraless")

    def __format__(self, format_spec: str) -> str:
        if format_spec in ["", "eraless", "epoch"]:
            if self.year < 0:
                return f"BDE.{-self.year}.{self.month:i}.{self.day}"
            else:
                return f"ADE.{self.year}.{self.month:i}.{self.day}"
        elif format_spec in ["era", "c", "canonical"]:
            return f"{self.era:i}.{self.erayear}.{self.month:i}.{self.day}"
        else:
            raise ValueError(f"Unknown format code '{format_spec}' for object of type '{type(self)}'")

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

    def __add__(self, other: 'DateDelta') -> T.Self:
        if isinstance(other, DateDelta):
            year, month, day = _reconcile_date_arithmatic(self._getstate(), other._getstate())
            return type(self)(year, month, day)
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other: T.Self | 'DateDelta') -> 'DateDelta' | T.Self:
        if isinstance(other, Date):
            pass  # TODO
        elif isinstance(other, DateDelta):
            return self + -other
        else:
            return NotImplemented

    def __hash__(self) -> int:
        "Hash."
        if self._hashcode == -1:
            yhi, ylo = divmod(self._year, 256)
            self._hashcode = hash(bytes([yhi, ylo, self._month, self._day]))
        return self._hashcode

    # Read-only field accessors
    @property
    def era(self) -> 'Era':
        for era in Era:
            if (
                (era.start is None or era.start <= self)
                and (era.end is None or self < era.end)
            ):
                return era
        else:
            raise RuntimeError(f"No matching Era found, '{Era}' may be illformed.")

    @property
    def year(self) -> int:
        return self._year

    @property
    def erayear(self) -> int:
        e_year = self.year
        if self.era.start is not None:
            e_year -= self.era.start.year
        if self.era.negated:
            return -e_year
        else:
            return e_year

    @property
    def month(self) -> 'Month':
        return Month(self._month)

    @property
    def inignemonth(self) -> 'InigneMonth':
        return InigneMonth(self._month)

    @property
    def day(self) -> int:
        return self._day

    @property
    def weekday(self) -> 'Day':
        wd = self._day % 6
        if wd == 0:
            wd = 6
        return Day(wd)

    @property
    def inigneweekday(self) -> 'InigneDay':
        wd = self._day % 6
        if wd == 0:
            wd = 6
        return InigneDay(wd)

    def _getstate(self) -> tuple[int, int, int]:
        return (self._year, self._month, self._day)

    __getnewargs__ = _getstate


class DateDelta():
    """Represent the difference between two Date objects.

    Supported operators:

    - add, subtract DateDelta
    - unary plus, minus, abs
    - compare to DateDelta
    - multiply, divide by int

    In addition, Date supports subtraction of two Date objects
    returning a DateDelta, and addition or subtraction of a Date
    and a DateDelta giving a Date.

    Representation: (years, days).
    """

    __slots__ = '_years', '_days'
    _years: int
    _days: int

    def __new__(cls, years: int = 0, days: int = 0) -> T.Self:
        assert isinstance(years, int)
        assert isinstance(days, int)
        self = object.__new__(cls)
        self._years = years
        self._days = days
        self._reconcile
        return self

    def _reconcile(self) -> None:
        d_years, m_days = divmod(self.asdays, _DAYS_IN_YEAR)
        if d_years < 0 and m_days > 0:
            d_years += 1
            m_days -= _DAYS_IN_YEAR
        self._years = d_years
        self._days = m_days

    @property
    def years(self) -> int:
        return self._years

    @property
    def months(self) -> int:
        d_months, m_days = divmod(self._days, _DAYS_IN_STANDARD_MONTH)
        if d_months < 0 and m_days > 0:
            return d_months + 1
        else:
            return d_months

    @property
    def days(self) -> int:
        d_months, m_days = divmod(self._days, _DAYS_IN_STANDARD_MONTH)
        if d_months < 0 and m_days > 0:
            return m_days - _DAYS_IN_STANDARD_MONTH
        else:
            return m_days

    @property
    def asyears(self) -> float:
        return self._years + (self._days / _DAYS_IN_YEAR)

    @property
    def asdays(self) -> int:
        return (self._years * _DAYS_IN_YEAR) + self._days

    @property
    def asstandardmonths(self) -> float:
        return self.asdays / _DAYS_IN_STANDARD_MONTH

    def __eq__(self, other) -> bool:
        if isinstance(other, DateDelta):
            return self._cmp(other) == 0
        else:
            return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, DateDelta):
            return self._cmp(other) <= 0
        else:
            return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, DateDelta):
            return self._cmp(other) < 0
        else:
            return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, DateDelta):
            return self._cmp(other) >= 0
        else:
            return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, DateDelta):
            return self._cmp(other) > 0
        else:
            return NotImplemented

    def _cmp(self, other: T.Self) -> T.Literal[-1, 0, 1]:
        assert isinstance(other, Date)
        return _cmp(self._getstate(), other._getstate())

    def __add__(self, other: T.Self | Date) -> T.Self | Date:
        if isinstance(other, DateDelta):
            return type(self)(self._years + other._years, self._days + other._days)
        elif isinstance(other, Date):
            return other.__add__(self)
        else:
            return NotImplemented

    def __neg__ (self) -> T.Self:
        return type(self)(days=-self.asdays)

    def _getstate(self) -> tuple[int, int]:
        return (self._years, self._days)


@enum.global_enum
class Day(_utils.PrettyEnumMixin, enum.IntEnum):
    # Standard days of the week
    RESDAY = 1
    FALDAY = 2
    ORDAY = 3
    CONDAY = 4
    EASDAY = 5
    PLADAY = 6


@enum.global_enum
class InigneDay(_utils.PrettyEnumMixin, enum.IntEnum):
    # Inigne days of the week
    RESDAY = 1
    FALDAY = 2
    ORDAY = 3
    CONDAY = 4
    STRADAY = 5
    WORDAY = 6


@enum.global_enum
class Month(_utils.PrettyEnumMixin, _utils.MonthMixin, enum.IntEnum):
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
class InigneMonth(_utils.PrettyEnumMixin, _utils.MonthMixin, enum.IntEnum):
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


_DRACONIC_EPOCH = Date(0, 7, 19)


@enum.global_enum
class Era(_utils.DataIntEnum):

    # Eras as referenceable objects
    ZEROTH = 0, "Before Dragons", None, _DRACONIC_EPOCH
    FIRST = 1, "Emergence", _DRACONIC_EPOCH, Date(720, 10, 21)
    SECOND = 2, "The Great Crusade", Date(720, 10, 21), Date(861, 6, 6)
    THIRD = 3, "Integration", Date(861, 6, 6), None

    def __init__(self, *args):
        if args[0] <= 0:
            self.negated = True
        else:
            self.negated = False
        self.short_name = self.name.capitalize()
        self.long_name = args[1]
        self.start = args[2]
        self.end = args[3]

    def __format__(self, format_spec: str) -> str:
        if format_spec == "s" or format_spec == "":
            return self.short_name
        elif format_spec == "l":
            return self.long_name
        elif format_spec == "i":
            return str(self.value)
        else:
            raise ValueError(f"Unknown format code '{format_spec}' for object of type '{type(self)}'")


@enum.global_enum
class ReferenceCalendars(_utils.DataEnum):
    BDE = _DRACONIC_EPOCH, None, True
    ADE = _DRACONIC_EPOCH, None, False

    def __init__(
            self,
            *args
    ) -> None:
        self.epoch = args[0]
        self.max = args[1]
        self.negated = args[2]
