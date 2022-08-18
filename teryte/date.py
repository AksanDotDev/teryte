import re
import datetime

DAYS_IN_EARTH_YEAR = 365


class TeryteDate():
    """Class to represent dates in Teryte"""
    _ANCHOR_AGE = 3
    _ANCHOR_YEAR = 1287
    AGE_LENGTHS = [False, 720, 141, False]
    STANDARD_MONTHS = 14
    MONTHS_IN_YEAR = 15
    DAYS_IN_YEAR = 348
    DAYS_IN_STANDARD_MONTH = 24
    DAYS_IN_FINAL_MONTH = 12
    _PATTERN = re.compile(
        r"(?P<age>\d)\.(?P<year>\d+)\.(?P<month>\d+)\.(?P<day>\d+)"
    )

    def __init__(self, age, year, month, day) -> None:
        self.age = age
        self.year = year
        self.month = month
        self.day = day

    def reconcile_date(self) -> None:
        if self.age < 0 or self.age >= len(TeryteDate.AGE_LENGTHS):
            raise ValueError("age undefined")
        y_day = TeryteDate.DAYS_IN_STANDARD_MONTH * (self.month - 1) + self.day

        while y_day < 1:
            self.year += 1 if self.age else -1
            y_day += TeryteDate.DAYS_IN_YEAR
        while y_day > TeryteDate.DAYS_IN_YEAR:
            self.year -= 1 if self.age else -1
            y_day -= TeryteDate.DAYS_IN_YEAR

        if self.age == 0 and self.year < 0:
            self.age += 1
            self.year = abs(self.year) - 1

        if self.age > 0:
            while self.age < len(TeryteDate.AGE_LENGTHS) - 1 \
                    and self.year > TeryteDate.AGE_LENGTHS[self.age]:
                self.year -= TeryteDate.AGE_LENGTHS[self.age] + 1
                self.age += 1
            while self.age > 0 and self.year < 0:
                self.age -= 1
                if self.age > 0:
                    self.year += TeryteDate.AGE_LENGTHS[self.age] + 1
                else:
                    self.year = abs(self.year) - 1
        y_day -= 1
        self.month = (y_day // TeryteDate.DAYS_IN_STANDARD_MONTH) + 1
        self.day = (y_day % TeryteDate.DAYS_IN_STANDARD_MONTH) + 1

    def valid_date(self) -> bool:
        if self.age < 0 or self.age >= len(TeryteDate.AGE_LENGTHS):
            return False
        elif self.year < 0 or self.year > TeryteDate.AGE_LENGTHS[self.age]:
            return False
        elif self.month <= 0 or self.month > TeryteDate.MONTHS_IN_YEAR:
            return False
        elif self.day <= 0 or self.day > TeryteDate.DAYS_IN_STANDARD_MONTH \
                or (self.month == TeryteDate.MONTHS_IN_YEAR
                    and self.day > TeryteDate.DAYS_IN_FINAL_MONTH):
            return False
        else:
            return True

    def todatetime(self):
        if self.age == 0:
            year = (-1 * self.year) - 1
            age = 1
        else:
            year = self.year
            age = self.age
        while age < TeryteDate._ANCHOR_AGE:
            year -= TeryteDate.AGE_LENGTHS[age] + 1
            age += 1
        # Note, expand if ages past 3 exist.

        year += TeryteDate._ANCHOR_YEAR
        base = datetime.date(year=year, month=1, day=1)

        y_day = TeryteDate.DAYS_IN_STANDARD_MONTH * (self.month - 1) + self.day
        y_day = int(y_day * (TeryteDate.DAYS_IN_YEAR/DAYS_IN_EARTH_YEAR))
        delta = datetime.timedelta(days=y_day-1)

        return base + delta

    def __str__(self) -> str:
        return f"{self.age}.{self.year}.{self.month}.{self.day}"

    def __repr__(self) -> str:
        return f"TeryteDate(age={self.age}, year={self.year}," + \
            f"month={self.month}, day={self.day})"

    @staticmethod
    def fromtoday():
        return TeryteDate.fromdatetime(
            datetime.date.today()
        )

    @staticmethod
    def fromdatetime(dt_input):
        age = TeryteDate._ANCHOR_AGE
        year = dt_input.year - TeryteDate._ANCHOR_YEAR
        y_day = (dt_input.month - 1)*29 + min(dt_input.day, 29) - 1
        month = (y_day // TeryteDate.DAYS_IN_STANDARD_MONTH) + 1
        day = (y_day % TeryteDate.DAYS_IN_STANDARD_MONTH) + 1
        protoype = TeryteDate(age, year, month, day)
        protoype.reconcile_date()
        return protoype

    @staticmethod
    def fromcommonformat(string):
        str_dict = TeryteDate._PATTERN.fullmatch(string).groupdict()
        return TeryteDate(
            **{key: int(value) for key, value in str_dict.items()}
        )
