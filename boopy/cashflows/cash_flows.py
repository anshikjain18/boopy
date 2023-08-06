import datetime
from abc import abstractmethod
from typing import Callable, Tuple, Union
import boopy.time.date.reference_date as reference_date_holder
from boopy.cashflows.cash_flow import has_occurred, trading_ex_coupon


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
        Calculates the Net Present Value, NPV, and Basis-Point Sensitivity, BPS. The NPV is the sum of the NPV of both legs and
        BPS is the amount the NPV changes if the rate changes by one basis point.

        References
        ----------
        cashflows.cpp
        https://quant.stackexchange.com/questions/20621/why-quantlib-computes-the-fixed-leg-swap-rate-by-this-formula
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
                df = term_structure._discount(coupon.payment_date)
                # Need to seperate the fixed and floating as floating needs the term structure.
                if type(coupon).__name__ == "FloatingRateLeg":
                    npv += coupon.amount(term_structure) * df
                else:
                    npv += coupon.amount() * df
                if coupon is not None:
                    bps += coupon.nominal * coupon.accrual_period() * df
        d = term_structure._discount(npv_date)
        npv /= d
        bps = 0.0001 * bps / d
        return npv, bps
