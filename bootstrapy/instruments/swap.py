import datetime

from typing import Callable, List


class Swap(object):
    def __init__(self):
        raise NotImplementedError

    def fixed_leg(self) -> None:
        """
        References
        ----------
        vanillaswap.cpp
        """
        raise NotImplementedError

    def ibor_leg(self) -> None:
        """
        References
        ----------
        vanillaswap.cpp
        """
        raise NotImplementedError

    def start_date(self, legs: List[Callable]) -> datetime.date:
        """
        Calculates the start date of the swap by investigating the cash flows of both legs.

        References
        ----------
        swap.cpp + ratehelpers.cpp
        """
        fixed_leg = legs[0]
        # Instead of implementing cash flow, we utilize the leg classes
        date = fixed_leg.start_date()
        for count, leg in legs:
            date = min(date, leg[count].start_date(count))
        return date

    def maturity_date(self) -> datetime.date:
        raise NotImplementedError
