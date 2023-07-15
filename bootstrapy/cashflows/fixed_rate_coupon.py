from typing import Callable, Union, List
import datetime
from bootstrapy.cashflows.coupons import Coupon
from bootstrapy.time.calendars.calendar import advance, adjust
from bootstrapy.time.calendars.utils import convert_period, is_period
from bootstrapy.time.frequency import Frequency
from bootstrapy.interest_rate import InterestRate, simple


class FixedRateCoupon(Coupon):
    def __init__(
        self,
        payment_date,
        nominal,
        rate,
        start_date,
        end_date,
        ref_date,
        ex_coupon_date,
    ):
        raise NotImplementedError


class FixedRateLeg:
    def __init__(
        self,
        fixed_schedule: Callable,
        payment_convention: Callable,
        payment_lag: int = 0,
        ex_coupon_period: Union[str, None] = None,
    ):
        self.fixed_schedule = fixed_schedule
        self.notionals = None
        self.payment_convention = payment_convention
        self.payment_lag = payment_lag
        self.coupon_rates = None
        self.ex_coupon_period = ex_coupon_period
        self.ex_coupon_adjustment = "Following"
        self.ex_coupon_end_of_month = False
        self.leg = []
        self.initialize()

    def with_coupon_rates(
        self,
        rate: List[Union[int, float]],
        day_count: Callable,
        compounding: Callable = simple,
        frequency: Callable = Frequency.ANNUAL,
    ) -> None:
        """
        Note there are three different version of this function for example one that takes vectors.
        Thus this one will always keep coupon_rates size to 1.
        References
        ----------
        fixedratecoupon.cpp
        """
        coupon_rates = [0]
        coupon_rates[0] = InterestRate(rate, day_count, compounding, frequency)
        self.coupon_rates = coupon_rates

    def with_notionals(self, notional: Union[float, int]) -> None:
        self.notionals = [notional]

    def initialize(self):
        start_date = self.fixed_schedule.dates[0]
        end_date = self.fixed_schedule.dates[1]
        payment_date = advance(end_date, self.payment_lag, "D", self.payment_convention)
        rate = self.coupon_rates[0]
        nominal = self.notionals[0]
        ex_coupon_date = None
        leg = []
        if is_period(self.ex_coupon_period) != True:
            ex_coupon_date = advance(
                payment_date, -self.ex_coupon_period, self.ex_coupon_adjustment
            )
        if (
            (self.fixed_schedule.has_tenor == True)
            & (self.fixed_schedule.has_is_regular == True)
            & (self.fixed_schedule.is_regular[1] != False)
        ):
            tenor_length, tenor_unit = convert_period(self.fixed_schedule.tenor)
            ref_date = advance(
                end_date, -tenor_length, tenor_unit, self.fixed_schedule.convention
            )
        else:
            ref_date = start_date
        leg.append(
            FixedRateCoupon(
                payment_date,
                nominal,
                rate,
                start_date,
                end_date,
                ref_date,
                ex_coupon_date,
            )
        )

        for i in range(2, len(self.fixed_schedule) - 1):
            start_date = end_date
            end_date = self.fixed_schedule.dates[i]
            payment_date = advance(
                end_date, self.payment_lag, "D", self.payment_convention
            )
            if is_period(self.ex_coupon_period):
                ex_coupon_date = advance(
                    payment_date, -self.ex_coupon_period, self.ex_coupon_adjustment
                )
            if (i - 1) < len(self.coupon_rates):
                rate = self.coupon_rates[i - 1]
            else:
                rate = self.coupon_rates[-1]
            if (i - 1) < len(self.notionals):
                nominal = self.notionals[i - 1]
            else:
                nominal = self.notionals[-1]
            leg.append(
                FixedRateCoupon(
                    payment_date,
                    nominal,
                    rate,
                    start_date,
                    end_date,
                    ref_date,
                    ex_coupon_date,
                )
            )
        if len(self.fixed_schedule) > 2:
            N = len(self.fixed_schedule)
            start_date = end_date
            end_date = self.fixed_schedule.dates[i]
            payment_date = advance(
                end_date, self.payment_lag, "D", self.payment_convention
            )
            if is_period(self.ex_coupon_period):
                ex_coupon_date = advance(
                    payment_date, -self.ex_coupon_period, self.ex_coupon_adjustment
                )
            if (N - 1) < len(self.coupon_rates):
                rate = self.coupon_rates[N - 2]
            else:
                rate = self.coupon_rates[-1]
            if (N - 1) < len(self.notionals):
                nominal = self.notionals[N - 2]
            else:
                nominal = self.notionals[-1]

            if (
                (self.fixed_schedule.has_tenor == True)
                & (self.fixed_schedule.has_is_regular == True)
                & (self.fixed_schedule.is_regular[1] != False)
            ):
                leg.append(
                    FixedRateCoupon(
                        payment_date,
                        nominal,
                        rate,
                        start_date,
                        end_date,
                        ref_date,
                        ex_coupon_date,
                    )
                )
            else:
                tenor_length, tenor_unit = convert_period(self.fixed_schedule.tenor)
                ref_date = advance(
                    start_date,
                    -tenor_length,
                    tenor_unit,
                    self.fixed_schedule.convention,
                )
                leg.append(
                    FixedRateCoupon(
                        payment_date,
                        nominal,
                        rate,
                        start_date,
                        end_date,
                        ref_date,
                        ex_coupon_date,
                    )
                )
        return leg
