from typing import Callable
from bootstrapy.instruments.vanilla_swap import VanillaSwap


class MakeVanillaSwap:
    """
    Helper class to make it easier to instantiate a vanilla swap.

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
        self.with_settlement_days = None
        self.with_fixed_leg_day_count = None
        self.with_fixed_leg_tenor = None
        self.with_fixed_leg_convention = None
        self.with_fixed_leg_termination_date_convention = None
        self.with_fixed_leg_calendar = None
        self.with_fixed_leg_end_of_month = None

        self.with_floating_leg_calendar = None
        self.with_floating_leg_end_of_month = None

        self.with_indexed_coupons = None

    def make_vanilla_swap(self) -> Callable:
        """
        Should return a vanilla_swap which inherits the original swap class.

        References
        ----------
        makevanillaswap.cpp + hpp
        """
        return VanillaSwap(
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
