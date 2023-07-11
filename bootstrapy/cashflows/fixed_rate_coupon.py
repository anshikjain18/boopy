from typing import Callable, Union
import datetime
from bootstrapy.cashflows.coupons import Coupon
from bootstrapy.time.calendars.calendar import advance, adjust
from bootstrapy.time.calendars.utils import convert_period


class FixedRateCoupon(Coupon):
    def __init__(self):
        raise NotImplementedError


class FixedRateLeg:
    def __init__(
        self,
        fixed_schedule: Callable,
        notional: float,
        fixed_rate: float,
        fixed_day_count: Callable,
        payment_convention: Callable,
        payment_lag: int = 0,
        ex_coupon_period: Union[str, None] = None,
    ):
        self.fixed_schedule = fixed_schedule
        self.notional = notional
        self.fixed_rate = fixed_rate
        self.fixed_day_count = fixed_day_count
        self.payment_convention = payment_convention
        self.payment_lag = payment_lag
        self.ex_coupon_period = ex_coupon_period
        self.leg = []
        self.initialize()

    def initialize(self):
        start_date = self.fixed_schedule.dates[0]
        end_date = self.fixed_schedule.dates[1]
        payment_date = advance(end_date, self.payment_lag, "D", self.payment_convention)
        rate = self.fixed_rate
        nominal = self.notional
        """
        if (self.ex_coupon_period != None):
            ex_coupon_date = advance(payment_date, -self.ex_coupon_period)
        """
        if (
            (self.fixed_schedule.has_tenor == True)
            & (self.fixed_schedule.has_is_regular == True)
            & (self.fixed_schedule.is_regular[1] != False)
        ):
            tenor_length, tenor_unit = convert_period(self.fixed_schedule.tenor)
            ref_date = advance(end_date, -tenor_length, tenor_unit self.fixed_schedule.convention)
        else:
            ref_date = start_date
