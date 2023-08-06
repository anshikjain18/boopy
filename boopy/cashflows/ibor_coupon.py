from typing import Callable, Union, List
from boopy.cashflows.cash_flow_vectors import FloatingLeg


class IborLeg:
    def __init__(self, schedule: Callable, index: Callable):
        self._schedule = schedule
        self._index = index
        self._notionals = None
        self._payment_day_counter = None
        self._payment_adjustments = None
        self._spreads = None
        self._use_indexed_coupons = None
        self._zero_payments = False
        self._ex_coupon_adjustment = "Unadjusted"
        self._is_in_arrears = False
        self._fixing_days = None

    def with_notionals(self, notional: Union[float, int]) -> None:
        self._notionals = notional

    def with_payment_day_counter(self, day_counter: Callable) -> None:
        self._payment_day_counter = day_counter

    def with_payment_adjustment(self, convention: str) -> None:
        self._payment_adjustments = convention

    def with_spreads(self, spread: Union[float, int]) -> None:
        self._spreads = spread

    def with_indexed_coupons(self, use_indexed_coupons: bool) -> None:
        self._use_indexed_coupons = use_indexed_coupons

    def _leg(self) -> List[Callable]:
        return FloatingLeg(
            self._schedule,
            self._notionals,
            self._index,
            self._payment_day_counter,
            self._payment_adjustments,
            self._spreads,
            self._zero_payments,
            self._ex_coupon_adjustment,
            self._is_in_arrears,
            self._fixing_days,
        )
