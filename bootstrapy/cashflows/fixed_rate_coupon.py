from typing import Callable, Union, List
import datetime
from bootstrapy.cashflows.coupons import Coupon
from bootstrapy.time.calendars.calendar import advance, adjust
from bootstrapy.time.calendars.utils import convert_period, is_period, multiply_period
from bootstrapy.time.frequency import Frequency
from bootstrapy.interest_rate import InterestRate


class FixedRateCoupon(Coupon):
    """
    Class for fixed rate coupons. Is called by the FixedRateLeg class when coupons are generated.
    """

    def __init__(
        self,
        payment_date,
        nominal,
        rate,
        accrual_start_date,
        accrual_end_date,
        ref_period_start,
        ref_period_end,
        ex_coupon_date,
    ):
        self.payment_date = payment_date
        self.nominal = nominal
        self.rate = rate
        self.accrual_start_date = accrual_start_date
        self.accrual_end_date = accrual_end_date
        self.ref_period_start = ref_period_start
        self.ref_period_end = ref_period_end
        self.ex_coupon_date = ex_coupon_date

    def accrual_period(self) -> Union[float, int]:
        """
        The return function should instead call the day counter class.
        """
        return self.rate.year_fraction(self.accrual_start_date, self.accrual_end_date)

    def amount(self) -> Union[float, int]:
        """
        Calculates the nominal multiplied with the rate that has compounded.
        References
        ----------
        fixedratecoupon.cpp
        """

        return self.nominal * (
            self.rate.compound_factor_accrual(
                self.accrual_start_date, self.accrual_end_date
            )
            - 1
        )


class FixedRateLeg:
    """
    Generates the coupons for a fixed rate leg.
    """

    def __init__(
        self,
        fixed_schedule: Callable,
        payment_convention: Callable,
        payment_lag: int = 0,
        ex_coupon_period: Union[str, None] = "0D",
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

    def with_coupon_rates(
        self,
        rate: List[Union[int, float]],
        day_count: Callable,
        compounding: str = "Simple",
        frequency: Callable = Frequency.ANNUAL.value,
    ) -> None:
        """
        Note there are three different version of this function for example one that takes vectors.
        Thus this one will always keep coupon_rates size to 1. Sets the rate for the fixed leg.
        References
        ----------
        fixedratecoupon.cpp
        """
        coupon_rates = [0]
        coupon_rates[0] = InterestRate(0, day_count, compounding, frequency)
        self.coupon_rates = coupon_rates

    def with_notionals(self, notional: Union[float, int]) -> None:
        self.notionals = [notional]

    def initialize(self):
        """
        Generates the coupons for the fixed rate leg by using the dates given by the Schedule class. The method is structure such as three cases are
        considered.
        - First coupon is added to the fixed leg.
        - All coupons with the expection of the last one is added to the fixed leg.
        - The last coupon is added to the fixed leg.
        """
        start_date = self.fixed_schedule.dates[0]
        end_date = self.fixed_schedule.dates[1]
        payment_date = advance(end_date, self.payment_lag, "D", self.payment_convention)
        rate = self.coupon_rates[0]
        nominal = self.notionals[0]
        ex_coupon_date = None
        leg = []
        # Preparing the first coupon.
        if is_period(self.ex_coupon_period) != True:
            ex_coupon_date = advance(
                payment_date, -self.ex_coupon_period, self.ex_coupon_adjustment
            )
        if (
            (self.fixed_schedule.has_tenor == True)
            & (self.fixed_schedule.has_is_regular == True)
            & (self.fixed_schedule.is_regular[0] != False)
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
                end_date,
                ex_coupon_date,
            )
        )
        # Preparing the rest of the coupons.
        for i in range(2, len(self.fixed_schedule) - 1):
            start_date = end_date
            end_date = self.fixed_schedule.dates[i]
            payment_date = advance(
                end_date, self.payment_lag, "D", self.payment_convention
            )
            if is_period(self.ex_coupon_period):
                ex_coupon_period = multiply_period(-1, self.ex_coupon_period)
                length, period = convert_period(ex_coupon_period)
                ex_coupon_date = advance(
                    payment_date,
                    length,
                    period,
                    self.ex_coupon_adjustment,
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
                    start_date,
                    end_date,
                    ex_coupon_date,
                )
            )
        if len(self.fixed_schedule) > 2:
            N = len(self.fixed_schedule)
            start_date = end_date
            end_date = self.fixed_schedule.dates[N - 1]
            payment_date = advance(
                end_date, self.payment_lag, "D", self.payment_convention
            )
            if is_period(self.ex_coupon_period):
                ex_coupon_period = multiply_period(-1, self.ex_coupon_period)
                length, period = convert_period(ex_coupon_period)
                ex_coupon_date = advance(
                    payment_date,
                    length,
                    period,
                    self.ex_coupon_adjustment,
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
                        start_date,
                        ref_date,
                        ex_coupon_date,
                    )
                )
        return leg
