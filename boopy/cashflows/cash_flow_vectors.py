from typing import Union, Callable, List
from boopy.time.calendars.calendar import advance, adjust
from boopy.time.calendars.utils import subtract_period, add_period, is_period
from boopy.cashflows.floating_rate_coupon import FloatingRateLeg
import datetime


def get(vector: List, i: int, default_value: Union[float, int]) -> Union[float, int]:
    """
    Corresponds to Quantlib detail::get.

    References
    ----------
    vectors.hpp
    """
    if isinstance(vector, list) is False:
        return default_value
    elif i < len(vector):
        return vector[i]
    else:
        return vector[-1]


def FloatingLeg(
    schedule: Callable,
    nominals: List[Union[float, int]],
    index: Callable,
    payment_day_counter: Callable,
    payment_adjustments: str,
    spreads: Union[float, int],
    is_zero: bool,
    ex_coupon_adjustment,
    is_in_arrears: bool,
    fixing_days: int,
    payment_lag=0,
    ex_coupon_period="0D",
    gearings: List = None,
    ex_coupon_date: datetime.date = None,
):
    n = len(schedule) - 1
    leg = [0] * n
    #    calendar = schedule.calendar
    last_payment_date = advance(
        schedule.dates[n], payment_lag, "D", payment_adjustments
    )
    for i in range(n):
        ref_start, start = schedule.dates[i], schedule.dates[i]
        ref_end, end = schedule.dates[i + 1], schedule.dates[i + 1]
        if is_zero is True:
            payment_date = last_payment_date
        else:
            payment_date = advance(end, payment_lag, "D", payment_adjustments)

        if (
            (i == 0)
            & (schedule.has_is_regular is True)
            & (schedule.has_tenor is True)
            & (schedule.is_regular[i] is False)
        ):
            temp_date = subtract_period(end, schedule.tenor)
            ref_start = adjust(temp_date, schedule.convention)
        if (
            (i == n - 1)
            & (schedule.has_is_regular is True)
            & (schedule.has_tenor is True)
            & (schedule.is_regular[i])
        ):
            temp_date = add_period(start + schedule.tenor)
            ref_end = adjust(temp_date, schedule.convention)
        if is_period(ex_coupon_period) != True:
            # if ex_coupon_calendar is empty then set ex_coupon_calendar to schedule.calendar
            ex_coupon_date = advance(
                payment_date, -ex_coupon_period, ex_coupon_adjustment
            )

        leg[i] = FloatingRateLeg(
            payment_date,
            get(nominals, i, 1),
            start,
            end,
            get(fixing_days, i, index.fixing_days),
            index,
            get(gearings, i, 1),
            get(spreads, i, 0),
            ref_start,
            ref_end,
            payment_day_counter,
            is_in_arrears,
            ex_coupon_date,
        )
    return leg
