import datetime
from abc import abstractmethod
from typing import Callable, Tuple, Union
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.cashflows.cash_flow import has_occurred, trading_ex_coupon


class Cashflows:
    @abstractmethod
    def start_date(leg: Callable) -> datetime.date:
        """
        Calculates the nearest accrual start date of each coupon given a leg.

        Reference
        ---------
        cashflows.cpp
        """
        d = datetime.date(5000, 1, 1)
        for coupon in leg:
            d = min(coupon.accrual_start_date, d)

        return d

    @abstractmethod
    def end_date(leg: Callable) -> datetime.date:
        """
        Calculates the last accrual start date of each coupon given a leg.
        References
        ----------
        cashflows.cpp
        """
        d = datetime.date(1, 1, 1)
        for coupon in leg:
            d = max(coupon.accrual_end_date, d)

        return d

    @abstractmethod
    def npvbps(
        leg: Callable,
        term_structure: Callable,
        include_settlement_date_flow: bool,
        settlement_date: datetime.date,
        npv_date: datetime.date,
    ) -> Tuple[Union[int, float]]:
        """
        Calculates the
        References
        ----------
        cashflows.cpp
        """
        npv = 0
        bps = 0

        if settlement_date == None:
            settlement_date = reference_date_holder.reference_date
        if npv_date is None:
            npv_date = settlement_date

        for coupon in leg:
            has_coupon_occurred = has_occurred(
                settlement_date, coupon, include_settlement_date_flow
            )
            is_trading_ex_coupon = trading_ex_coupon(settlement_date, coupon)
            if (has_coupon_occurred is False) & (is_trading_ex_coupon is False):
                df = term_structure.discount(coupon.payment_date)
                npv = NotImplementedError  # issue is with day counter at cash flow.
