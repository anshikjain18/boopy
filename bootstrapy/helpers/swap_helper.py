from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance, adjust
from typing import Callable


class SwapRateHelper(InterestRateHelper):
    def __init__(
        self,
        rate: float,
        tenor: str,
        calendar: Callable,
        frequency: Callable,
        day_counter: Callable,
        ibor_index: Callable,
        pillar: str = "last_relevant_date",
    ):
        super().__init__(day_counter)
        self.rate = rate
        self.timeunit = tenor[-1]
        self.length = int(tenor[: len(tenor) - 1])
        self.calendar = calendar
        self.frequency = frequency
        self.ibor_index = ibor_index
        self.pillar = pillar

    def make_vanilla_swap(self) -> None:
        """
        References
        ----------
        ratehelpers.hpp + cpp
        makevanillaswap.cpp
        """
        raise NotImplementedError

    def implied_quote(self) -> float:
        raise NotImplementedError
