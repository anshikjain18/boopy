import datetime
from abc import abstractmethod
from typing import Callable


class Cashflows:
    @abstractmethod
    def start_date(leg: Callable) -> datetime.date:
        """
        Calculates the nearest accrual start date of each coupon given a leg.

        Reference
        ---------
        cashflows.cpp
        """
        d = datetime.date(5000, 1, 1)
        for coupon in leg:
            d = min(coupon.accrual_start_date, d)

        return d

    @abstractmethod
    def end_date(leg: Callable) -> datetime.date:
        d = datetime.date(1, 1, 1)
        for coupon in leg:
            d = max(coupon.accrual_end_date, d)

        return d
