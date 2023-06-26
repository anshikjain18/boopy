import datetime
from bootstrapy.instruments.swap import Swap


class VanillaSwap(Swap):
    def __init__(
        self,
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
