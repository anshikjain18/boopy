from typing import Callable
from bootstrapy.time.calendars.calendar import adjust, advance
from bootstrapy.time.calendars.utils import year_fraction
from bootstrapy.time.date.maturity import time_from_reference
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
        self.period = period
        self.settlement_days = settlement_days
        self.timeunit = period[-1]
        self.length = int(period[: len(period) - 1])
        self.calendar = calendar
        self.convention = convention
        self.day_count = day_count
        # Should be removed in the future to avoid confusiong
        self.fixing_days = settlement_days

    def year_fraction(self, d1: datetime.date | None, d2: datetime.date) -> float:
        """
        Calculates the year fraction. If d1 is equal to d1, then assume it will be the
        year fraction using the reference date.

        This class has now been moved to calendars utils.py. Move all references of this function.
        Parameters
        ----------

        """

        if d1 == None:
            d1 = 0
            d2_int = time_from_reference(None, d2)
            return self.day_count(0, d2_int)
        else:
            d1_int = time_from_reference(None, d1)
            d2_int = time_from_reference(None, d2)
            return self.day_count(d1_int, d2_int)

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

    def forecast_fixing_with_dates(
        self, d1: datetime.date, d2: datetime.date, term_structure: Callable
    ) -> float:
        """
        Mimics the behavior of forecast_fixing but with the addition of dates as input
        """
        t = self.year_fraction(d1, d2)
        df_2 = term_structure._discount(d2)
        df_1 = term_structure._discount(d1)
        return (df_1 / df_2 - 1) / t

    def forecast_fixing(
        self, TermStructure: Callable, fixing_date: datetime.date
    ) -> float:
        """
        Calculates the forward rate using d1 and d2. t is the time between d1 and d2 using the instruments
        day count convention.

        References
        ----------
        Calls discountImpl which will return exp(-r*t). However first r is calculated through calling value from interpolation.
            iborindex.hpp

        Parameters
        ----------

        """
        d1 = self.value_date(fixing_date)
        d2 = self.maturity_date(d1)
        t = self.year_fraction(d1, d2)
        df_2 = TermStructure._discount(d2)
        df_1 = TermStructure._discount(d1)
        return (df_1 / df_2 - 1) / t
