from typing import Callable
from bootstrapy.time.calendars.calendar import adjust, advance
from bootstrapy.time.calendars.utils import year_fraction
import datetime


class IborIndex:
    def __init__(
        self,
        settlement_days: int,
        period: str,
        convention: str,
        day_count: Callable,
        calendar: Callable = None,  # will be rewritten, now only Swedish Calendar works
    ):
        self.settlement_days = settlement_days
        self.timeunit = period[-1]
        self.length = int(period[: len(period) - 1])
        self.calendar = calendar
        self.convention = convention
        self.day_count = day_count

    def value_date(self, date: datetime.date) -> datetime.date:
        """
        Calculates the value date of the ibor index given a date.

        References
        ----------
        interestrateindex.hpp
        """
        return advance(date, self.settlement_days, "D", self.convention)

    def maturity_date(self, date: datetime.date) -> datetime.date:
        """
        Calculates the maturity date of the ibor index given a date.

        References
        ----------
        iborindex.cpp
        """
        return advance(date, self.length, self.timeunit, self.convention)

    def fixing_date(self, date: datetime.date) -> datetime.date:
        """
        Calculates the fixing date given a date.

        References
        ----------
        interestrateindex.hpp
        ratehelpers.cpp
        """
        return advance(date, -self.settlement_days, "D", self.convention)

    def forecast_fixing(self, fixing_date: datetime.date) -> datetime.date:
        d1 = self.value_date(fixing_date)
        d2 = self.maturity_date(d1)
        t = year_fraction(d1, d2)
        raise NotImplementedError
