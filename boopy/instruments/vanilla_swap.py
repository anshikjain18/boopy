import datetime
from boopy.instruments.swap import Swap
from typing import Callable, Union
from boopy.cashflows.fixed_rate_coupon import FixedRateLeg
from boopy.cashflows.ibor_coupon import IborLeg


class VanillaSwap(Swap):
    def __init__(
        self,
        type: str,
        nominal: Union[float, int],
        fixed_schedule: Callable,
        rate: Union[float, int],
        fixed_day_count: Callable,
        float_schedule: Callable,
        ibor_index: Callable,
        spread: Union[float, int],
        float_day_count: Callable,
        payment_convention: Callable,
        use_indexed_coupon,
    ):
        self.legs = [0, 0]

        # Define fixed leg
        if payment_convention is None:
            payment_convention = float_schedule.convention

        fixed_leg = FixedRateLeg(
            fixed_schedule,
            payment_convention,
        )
        fixed_leg.with_coupon_rates(rate, fixed_day_count)
        fixed_leg.with_notionals(nominal)
        fixed_leg = fixed_leg.initialize()
        self.legs[0] = fixed_leg

        # Define floating leg
        float_leg = IborLeg(float_schedule, ibor_index)

        float_leg.with_notionals(nominal)
        float_leg.with_payment_day_counter(ibor_index.day_count)
        float_leg.with_payment_adjustment(payment_convention)
        float_leg.with_spreads(spread)
        float_leg.with_indexed_coupons(use_indexed_coupon)
        float_leg = float_leg._leg()
        self.legs[1] = float_leg

        def setup_arguments(self) -> None:
            raise NotImplementedError
