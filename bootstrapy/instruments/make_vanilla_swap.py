from typing import Callable
from bootstrapy.instruments.vanilla_swap import VanillaSwap
from bootstrapy.time.schedule import Schedule
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance, adjust
from bootstrapy.time.calendars.utils import str_to_datetime, add_period


class MakeVanillaSwap:
    """
    Helper class to make it easier to instantiate a vanilla swap.

    TODO: Remove with_... naming convention

    References
    ----------
    makevanillaswap.cpp + hpp
    """

    def __init__(
        self, tenor: str, ibor_index: Callable, fwd_start: str, fixed_rate: float = "0D"
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
        self.with_fixed_leg_end_of_month = False

        self.with_floating_leg_calendar = None
        self.with_floating_leg_end_of_month = False
        self.with_effective_date = None

        self.with_indexed_coupons = None
        self.with_termination_date = None
        self.spread = 0
        self.fixed_rule = "backward"
        self.float_rule = "backward"

        self.fixed_first_date = None
        self.fixed_next_to_last_date = None

        self.float_first_date = None
        self.float_next_to_last_date = None
        self.initialize_dates()
        self.fixed_schedule = None
        self.float_schedule = None

    def initialize_dates(self) -> None:
        """
        Calculates the dates for creating the schedule of the coupons.

        References
        ----------
        makevanillaswap.cpp
        """

        if self.with_effective_date != None:
            start_date = str_to_datetime(self.with_effective_date)
        else:
            ref_date = str_to_datetime(reference_date_holder.reference_date)
            ref_date = adjust(
                ref_date, self.ibor_index.convention
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
            start_date = add_period(spot_date, self.fwd_start)
            """
            add if and else statement for self.fwd_start, see makevanillaswap.cpp            
            """

        end_date = self.with_termination_date
        if end_date == None:
            if self.with_floating_leg_end_of_month:
                raise NotImplementedError
                # end_date = adjust(self.start_date, self.tenor, 'ModifiedFollowing', )
            else:
                end_date = add_period(start_date, self.tenor)

        # Creates the schedules for the coupons
        self.fixed_schedule = Schedule(
            start_date,
            end_date,
            self.with_fixed_leg_tenor,
            self.with_fixed_leg_calendar,
            self.with_fixed_leg_convention,
            self.with_fixed_leg_termination_date_convention,
            self.fixed_rule,
            self.with_fixed_leg_end_of_month,
            self.fixed_first_date,
            self.fixed_next_to_last_date,
        )
        # Revisit and rewrite properly
        self.float_schedule = Schedule(
            start_date,
            end_date,
            self.ibor_index.period,
            self.ibor_index.calendar,
            self.ibor_index.convention,
            self.ibor_index.convention,
            self.float_rule,
            self.with_floating_leg_end_of_month,
            self.float_first_date,
            self.float_next_to_last_date,
        )

    def make_vanilla_swap(self) -> Callable:
        """
        Should return a vanilla_swap which inherits the original swap class.

        References
        ----------
        makevanillaswap.cpp + hpp
        """

        vanilla_swap = VanillaSwap(
            "payer",
            1,
            self.fixed_schedule,
            self.fixed_rate,
            self.with_fixed_leg_day_count,
            self.float_schedule,
            self.ibor_index,
            self.spread,
            self.with_fixed_leg_day_count,
            None,
            self.with_indexed_coupons,
        )

        return vanilla_swap
