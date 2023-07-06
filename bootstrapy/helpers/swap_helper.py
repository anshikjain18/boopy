from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import maturity_int
from bootstrapy.time.calendars.calendar import advance, adjust
from typing import Callable
from bootstrapy.instruments.make_vanilla_swap import MakeVanillaSwap


class SwapHelper(InterestRateHelper):
    def __init__(
        self,
        rate: float,
        tenor: str,
        convention: Callable,
        frequency: Callable,
        day_counter: Callable,
        ibor_index: Callable,
        pillar: str = "last_relevant_date",
        fwd_start: str = "0D",
        calendar: Callable = None,  # To be written, now only the swedish calendar works
        end_of_month: bool = False,
        settlement_day=None,
        use_indexed_coupons=None,
    ):
        super().__init__(day_counter)
        self.rate = rate
        self.tenor = tenor
        self.convention = convention
        self.timeunit = tenor[-1]
        self.length = int(tenor[: len(tenor) - 1])
        self.fwd_start = fwd_start
        self.calendar = calendar
        self.frequency = frequency
        self.ibor_index = ibor_index
        self.end_of_month = end_of_month
        self.pillar = pillar
        self.settlement_day = settlement_day
        self.use_indexed_coupons = use_indexed_coupons

        self.vanilla_swap = self.make_vanilla_swap()

    def make_vanilla_swap(self) -> None:
        """
        References
        ----------
        ratehelpers.hpp + cpp
        makevanillaswap.cpp
        """
        vanilla_swap = self.vanilla_swap = MakeVanillaSwap(
            self.tenor, self.ibor_index, self.fwd_start, self.rate
        )
        self.vanilla_swap.with_settlement_days = self.settlement_day
        self.vanilla_swap.with_fixed_leg_day_count = self.day_count
        self.vanilla_swap.with_fixed_leg_tenor = self.tenor
        self.vanilla_swap.with_fixed_leg_convention = self.convention
        self.vanilla_swap.with_fixed_leg_termination_date_convention = self.convention
        self.vanilla_swap.with_fixed_leg_calendar = self.calendar
        self.vanilla_swap.with_fixed_leg_end_of_month = self.end_of_month
        self.vanilla_swap.with_floating_leg_calendar = self.calendar
        self.vanilla_swap.with_floating_leg_end_of_month = self.end_of_month
        self.vanilla_swap.with_indexed_coupons = self.use_indexed_coupons
        return vanilla_swap

    def implied_quote(self) -> float:
        raise NotImplementedError
