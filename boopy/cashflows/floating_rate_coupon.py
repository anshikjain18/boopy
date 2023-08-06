from typing import List, Union, Callable
from boopy.cashflows.coupons import Coupon
import datetime


class FloatingRateLeg(Coupon):
    def __init__(
        self,
        payment_date: datetime.date,
        nominal: Union[float, int],
        start_date: datetime.date,
        end_date: datetime.date,
        fixing_days: int,
        index: Callable,
        gearing,
        spread: Union[float, int],
        ref_period_start: datetime.date,
        ref_period_end: datetime.date,
        day_counter: Callable,
        is_in_arrears: bool,
        ex_coupon_date: datetime.date,
    ):
        super().__init__(
            payment_date,
            nominal,
            start_date,
            end_date,
            ref_period_start,
            ref_period_end,
            ex_coupon_date,
        )

        self.payment_date = payment_date
        self.nominal = nominal
        self.start_date = start_date
        self.end_date = end_date
        self._fixing_days = fixing_days
        self._index = index
        self._gearing = gearing
        self._spread = spread
        self._ref_period_start = ref_period_start
        self._ref_period_end = ref_period_end
        self._day_counter = day_counter
        self._is_in_arrears = is_in_arrears
        self._ex_coupon_date = ex_coupon_date

    def index_fixing(self, term_structure) -> Union[float, int]:
        return self._index.forecast_fixing_with_dates(
            self.accrual_start_date, self.accrual_end_date, term_structure
        )

    def adjusted_fixing(self, term_structure) -> Union[float, int]:
        return self.index_fixing(term_structure)

    def accrual_period(self) -> Union[float, int]:
        return self._day_counter(self.accrual_start_date, self.accrual_end_date)

    def rate(self, term_structure) -> Union[float, int]:
        """
        Here rate is simplified in comparison to the QuantLib implementation.
        """
        return self._gearing * self.adjusted_fixing(term_structure) + self._spread

    def amount(self, term_structure: Callable) -> Union[float, int]:
        accrual_period = self._day_counter(
            self.accrual_start_date, self.accrual_end_date
        )
        return self.nominal * accrual_period * self.rate(term_structure)
