from bootstrapy.instruments.swap import Swap
from typing import Callable
import datetime
from bootstrapy.instruments.swap import SwapEngine
from bootstrapy.time.calendars.utils import str_to_datetime
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.cashflows.cash_flows import Cashflows


class DiscountingSwapEngine(SwapEngine):
    def __init__(
        self,
        term_structure: Callable,
        vanilla_swap: Callable,
        include_settlement_date_flows: bool = None,
        settlement_date: datetime.date = None,
        npv_date: datetime.date = None,
    ):
        self.term_structure = term_structure
        self.include_settlement_date_flows = include_settlement_date_flows
        self.settlement_date = settlement_date
        self.npv_date = npv_date
        self.vanilla_swap = vanilla_swap

    def calculate(self):
        self.value = 0
        self.error_estimate = None
        self.payer = [-1, 1]
        ref_date = reference_date_holder.reference_date

        if self.settlement_date is None:
            self.settlement_date = ref_date

        self.valuation_date = self.npv_date
        if self.npv_date is None:
            self.valuation_date = ref_date
        self.npv_date_discount = self.term_structure._discount(self.valuation_date)
        n = len(self.vanilla_swap.legs)
        self.legNPV = [0] * n
        self.legBPS = [0] * n
        for i in range(n):
            self.legNPV[i], self.legBPS[i] = Cashflows.npvbps(
                self.vanilla_swap.legs[i],
                self.term_structure,
                False,
                self.settlement_date,
                self.npv_date,
            )
            self.legNPV[i] *= self.payer[i]
            self.legBPS[i] *= self.payer[i]
        self.value += self.legNPV[i]
