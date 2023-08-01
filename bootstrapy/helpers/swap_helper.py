from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import maturity_int
from bootstrapy.time.calendars.calendar import advance, adjust
from typing import Callable
from bootstrapy.instruments.make_vanilla_swap import MakeVanillaSwap
from bootstrapy.cashflows.cash_flows import Cashflows
from bootstrapy.pricing.swap.discountingswapengine import DiscountingSwapEngine
from bootstrapy.instruments.swap import Swap


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
        pillar_choice: str = "latest_relevant_date",
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
        self.pillar_choice = pillar_choice

        self.latest_date = None
        self.pillar_date = None
        self.vanilla_swap = self.make_vanilla_swap()
        self.initialize_dates()
        self.quote = rate

    def initialize_dates(self) -> None:
        earliest_date = Swap.start_date(self.vanilla_swap.legs)
        maturity_date = Swap.maturity_date(self.vanilla_swap.legs)
        latest_relevant_date = maturity_date  # Actually suppose to compare the last floating but it is not needed if you are not implementing a new coupon pricer according to Quantlib
        match self.pillar_choice:
            case "maturity_date":
                self.pillar_date = maturity_date

            case "latest_relevant_date":
                self.pillar_date = latest_relevant_date
            case "custom_date":
                raise NotImplementedError
        self.latest_date = self.pillar_date

    def make_vanilla_swap(self) -> None:
        """
        References
        ----------
        ratehelpers.hpp + cpp
        makevanillaswap.cpp
        """
        make_vanilla_swap_class = MakeVanillaSwap(
            self.tenor, self.ibor_index, self.fwd_start, self.rate
        )
        # Below needs to be rewritten
        make_vanilla_swap_class.with_fixed_leg_tenor(self.tenor)
        make_vanilla_swap_class.with_settlement_days = self.settlement_day
        make_vanilla_swap_class.with_fixed_leg_day_count = self.day_count
        make_vanilla_swap_class.with_fixed_leg_tenor = self.tenor
        make_vanilla_swap_class.with_fixed_leg_convention = self.convention
        make_vanilla_swap_class.with_fixed_leg_termination_date_convention = (
            self.convention
        )
        make_vanilla_swap_class.with_fixed_leg_calendar = self.calendar
        make_vanilla_swap_class.with_fixed_leg_end_of_month = self.end_of_month
        make_vanilla_swap_class.with_floating_leg_calendar = self.calendar
        make_vanilla_swap_class.with_floating_leg_end_of_month = self.end_of_month
        make_vanilla_swap_class.with_indexed_coupons = self.use_indexed_coupons
        make_vanilla_swap_class.init_make_vanilla_swap()

        vanilla_swap = make_vanilla_swap_class.make_vanilla_swap()

        return vanilla_swap

    def implied_quote(self, term_structure: Callable) -> float:
        engine = DiscountingSwapEngine(term_structure, self.vanilla_swap)
        engine.calculate()
        basis_point = 0.0001
        floating_leg_npv = engine.legNPV[1]
        result = -floating_leg_npv / (engine.legBPS[0] / basis_point)
        return result
