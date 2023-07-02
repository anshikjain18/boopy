import datetime
from bootstrapy.instruments.swap import Swap
from typing import Callable


class VanillaSwap(Swap):
    def __init__(
        self,
        fixed_rate: float,
        ibor_index: Callable,
        settlement_days,
        fixed_day_counter,
        fixed_tenor,
        fixed_convention,
        fixed_leg_termination_date_convention,
        fixed_leg_calendar,
        fixed_leg_end_of_month,
        floating_leg_calendar,
        floating_leg_end_of_month,
        indexed_coupons,
    ):
        self.settlement_days_ = settlement_days
        self.fixed_day_count_ = fixed_day_counter
        self.fixed_tenor_ = fixed_tenor
        self.fixed_convention_ = fixed_convention
        self.fixed_termination_date_convention_ = fixed_leg_termination_date_convention
        self.fixed_leg_calendar_ = fixed_leg_calendar
        self.fixed_leg_end_of_month_ = fixed_leg_end_of_month
        self.floating_leg_calendar_ = floating_leg_calendar
        self.floating_leg_end_of_month_ = floating_leg_end_of_month
        self.indexed_coupons_ = indexed_coupons

        self.nominal = 1
        self.legs = [0] * 2
        fixed_schedule, payment_convention = 0, 0  # To be implemented
        self.legs[0] = self.FixedRateLeg(
            fixed_schedule,
            self.nominal,
            fixed_rate,
            fixed_day_counter,
            payment_convention,
        )
        floating_schedule = 0  # To be implemented
        self.legs[1] = self.ibor_leg(
            floating_schedule,
            self.nominal,
            ibor_index.day_count,
            payment_convention,
            self.indexed_coupons_,
        )

        def setup_arguments(self) -> None:
            raise NotImplementedError
