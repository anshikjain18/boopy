from typing import List, Union, Callable
from bootstrapy.cashflows.coupons import Coupon
import datetime


class FloatingRateLeg(Coupon):
    def __init__(
        self,
        payment_date: datetime.date,
        nominal: Union[float, int],
        start_date: datetime.date,
        end_date: datetime.date,
        fixing_days: int,
        index: Callable,
        gearing,
        spread: Union[float, int],
        ref_period_start: datetime.date,
        ref_period_end: datetime.date,
        day_counter: Callable,
        is_in_arrears: bool,
        ex_coupon_date: datetime.date,
    ):
        super().__init__(
            payment_date,
            nominal,
            start_date,
            end_date,
            ref_period_start,
            ref_period_end,
            ex_coupon_date,
        )

        self.payment_date = payment_date
        self.nominal = nominal
        self.start_date = start_date
        self.end_date = end_date
        self._fixing_days = fixing_days
        self._index = index
        self._gearing = gearing
        self._spread = spread
        self._ref_period_start = ref_period_start
        self._ref_period_end = ref_period_end
        self._day_counter = day_counter
        self._is_in_arrears = is_in_arrears
        self._ex_coupon_date = ex_coupon_date
