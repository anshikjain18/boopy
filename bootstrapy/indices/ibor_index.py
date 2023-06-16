from typing import Callable
from bootstrapy.bootstrap.time.calendars.calendar import adjust, advance
import datetime
class IborIndex:
    def __init__(self, 
                 settlement_days : int,
                 period : str,
                 calendar : Callable,
                 convention : str,
                 day_count : Callable):
        self.settlement_days = settlement_days
        self.timeunit = period[-1]
        self.length = int(period[:len(period)-1])
        self.calendar = calendar
        self.convention = convention
        self.day_count = day_count

    def fixing_date(self, date : datetime.date) -> datetime.date:
        """
        Calculates the fixing date given a date.

        References
        ----------
        interestrateindex.hpp
        ratehelpers.cpp
        """
        return advance(date, -self.settlement_days, 'D', self.convention)
