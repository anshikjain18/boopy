from typing import Callable


# Also known as the Iborleg
class FloatLeg:
    def __init__(
        self,
        float_schedule: Callable,
        ibor_index: Callable,
        notional: float,
        float_day_count: Callable,
        payment_convention: Callable,
        use_indexed_coupons: bool,
    ):
        self.ibor_index = ibor_index
        self.float_schedule = float_schedule
        self.notional = notional
        self.float_day_count = float_day_count
        self.payment_convention = payment_convention
        self.use_indexed_coupons = use_indexed_coupons

    def start_date(self):
        raise NotImplementedError
