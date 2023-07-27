import datetime
from typing import Callable
import bootstrapy.time.date.reference_date as reference_date_holder


def has_occurred(
    ref_date: datetime.date, coupon: Callable, include_ref_date: bool
) -> bool:
    """
    Given a reference date calculates if the coupon has occurred or not.

    References
    ----------
    cashflow.cpp
    """
    if ref_date != None:
        payment_date = coupon.payment_date
        if ref_date < payment_date:
            return False
        elif ref_date > payment_date:
            return True
    else:
        return ValueError("Reference date is incorrectly set.")


def trading_ex_coupon(ref_date: datetime.date, coupon: Callable) -> bool:
    ecd = coupon.ex_coupon_date
    if isinstance(ecd, datetime.date):
        return False

    if isinstance(ref_date, datetime.date):
        ref = ref_date
    else:
        ref = reference_date_holder.reference_date
    return ecd <= ref
