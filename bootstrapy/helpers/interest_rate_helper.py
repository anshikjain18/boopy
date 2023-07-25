import datetime
from typing import Callable
from bootstrapy.time.date.maturity import time_from_reference


class InterestRateHelper:
    def __init__(
        self,
        day_count: Callable[[int, int], float],
    ):
        self.day_count = day_count

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
