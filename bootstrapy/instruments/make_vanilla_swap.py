from typing import Callable
from bootstrapy.instruments.vanilla_swap import VanillaSwap
from bootstrapy.time.schedule import Schedule
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance, adjust


class MakeVanillaSwap:
    """
    Helper class to make it easier to instantiate a vanilla swap.

    TODO: Remove with_...

    References
    ----------
    makevanillaswap.cpp + hpp
    """

    def __init__(
        self,
        tenor: str,
        ibor_index: Callable,
        fwd_start: str,
        fixed_rate: float = 0,
    ):
        self.tenor = tenor
        self.ibor_index = ibor_index
        self.fwd_start = fwd_start
        self.fixed_rate = fixed_rate

        self.with_settlement_days = None
        self.with_fixed_leg_day_count = None
        self.with_fixed_leg_tenor = None
        self.with_fixed_leg_convention = None
        self.with_fixed_leg_termination_date_convention = None
        self.with_fixed_leg_calendar = None
        self.with_fixed_leg_end_of_month = None

        self.with_floating_leg_calendar = None
        self.with_floating_leg_end_of_month = None
        self.with_effective_date = None

        self.with_indexed_coupons = None

    def initialize_dates(self) -> Callable:
        """
        Calculates the dates for creating the schedule of the coupons.

        References
        ----------
        makevanillaswap.cpp
        """
        if self.with_effective_date != None:
            start_date = self.with_effective_date
        else:
            ref_date = reference_date_holder.reference_date
            ref_date = adjust(
                ref_date
            )  # Should be floating leg calendar as the legs can have different calendars.
            if self.with_settlement_days == None:
                spot_date = self.ibor_index.value_date(ref_date)
            else:
                spot_date = advance(
                    ref_date,
                    self.with_settlement_days,
                    "D",
                    self.with_fixed_leg_convention,
                )

    def make_vanilla_swap(self) -> Callable:
        """
        Should return a vanilla_swap which inherits the original swap class.

        References
        ----------
        makevanillaswap.cpp + hpp
        """

        vanilla_swap = VanillaSwap(
            self.with_settlement_days,
            self.with_fixed_leg_day_count,
            self.with_fixed_leg_tenor,
            self.with_fixed_leg_convention,
            self.with_fixed_leg_termination_date_convention,
            self.with_fixed_leg_calendar,
            self.with_fixed_leg_end_of_month,
            self.with_floating_leg_calendar,
            self.with_floating_leg_end_of_month,
            self.with_indexed_coupons,
        )
        return vanilla_swap
