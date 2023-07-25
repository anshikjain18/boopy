from bootstrapy.instruments.swap import Swap
from typing import Callable
import datetime
from bootstrapy.instruments.swap import SwapEngine

import bootstrapy.time.date.reference_date as reference_date_holder


class DiscountingSwapEngine(SwapEngine):
    def __init__(
        self,
        term_structure: Callable,
        include_settlement_date_flows: bool = None,
        settlement_date: datetime.date = None,
        npv_date: datetime.date = None,
    ):
        self.term_structure = term_structure
        self.include_settlement_date_flows = include_settlement_date_flows
        self.settlement_date = settlement_date
        self.npv_date = npv_date

    def calculate(self):
        self.value = 0
        self.error_estimate = None

        ref_date = reference_date_holder.reference_date

        if self.settlement_date is None:
            self.settlement_date = ref_date

        self.valuation_date = self.npv_date
        if self.npv_date is None:
            self.valuation_date = ref_date
