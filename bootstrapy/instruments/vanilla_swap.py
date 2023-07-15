import datetime
from bootstrapy.instruments.swap import Swap
from typing import Callable, Union
from bootstrapy.cashflows.fixed_rate_coupon import FixedLeg
from bootstrapy.cashflows.fixed_rate_coupon import FixedLeg


class VanillaSwap(Swap):
    def __init__(
        self,
        type,
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
        self.legs[0] = (
            FixedLeg(
                fixed_schedule,
                payment_convention,
            )
            .with_coupon_rates(rate, fixed_day_count)
            .with_notionals(nominal)
        )
        self.legs[1] = IborLeg(
            float_schedule,
            nominal,
            ibor_index.day_count,
            payment_convention,
            use_indexed_coupon,
        )

        def setup_arguments(self) -> None:
            raise NotImplementedError
