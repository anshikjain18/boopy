import datetime
from typing import Union


class Coupon:
    def __init__(
        self,
        payment_date: datetime.date,
        nominal: Union[float, int],
        accrual_start_date: datetime.date,
        accrual_end_date: datetime.date,
        ref_period_start: Union[datetime.date, None] = None,
        ref_period_end: Union[datetime.date, None] = None,
        ex_coupon_date: Union[datetime.date, None] = None,
    ):
        self.payment_date = payment_date
        self.nominal = nominal
        self.accrual_start_date = accrual_start_date
        self.accrual_end_date = accrual_end_date
        self.ref_period_start = ref_period_start
        self.ref_period_end = ref_period_end
        self.ex_coupon_date = ex_coupon_date
