from typing import Callable


class FixedLeg:
    def __init__(
        self,
        fixed_schedule: Callable,
        notional: float,
        fixed_rate: float,
        fixed_day_count: Callable,
        payment_convention: Callable,
    ):
        self.fixed_schedule = fixed_schedule
        self.notional = notional
        self.fixed_rate = fixed_rate
        self.fixed_day_count = fixed_day_count
        self.payment_convention = payment_convention

    def start_date(self):
        raise NotImplementedError
