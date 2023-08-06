import datetime
from abc import abstractmethod
from typing import Callable, List
from boopy.cashflows.cash_flows import Cashflows
from boopy.instruments.instrument import InstrumentArguments, InstrumentResults


class SwapArguments(InstrumentArguments):
    def __init__(self):
        super().__init__()
        self.legs = None
        self.payer = None


class SwapResults(InstrumentResults):
    def __init__(self):
        super().__init__()
        self.legNPV = None
        self.legBPS = None
        self.start_discount = None
        self.end_discount = None
        self.npv_date_discount = None


class SwapEngine(SwapResults, SwapArguments):
    def __init__(self):
        super().__init__()


class Swap(object):
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def start_date(legs: List[Callable]) -> datetime.date:
        """
        Calculates the start date of the swap by investigating the cash flows of both legs.

        References
        ----------
        swap.cpp + ratehelpers.cpp
        """
        fixed_leg = legs[0]
        # Instead of implementing cash flow, we utilize the leg classes
        date = Cashflows.start_date(fixed_leg)
        for idx in range(1, len(legs)):
            date = min(date, Cashflows.start_date(legs[idx]))
        return date

    @abstractmethod
    def maturity_date(legs: List[Callable]) -> datetime.date:
        """
        Calculates the maturity date of the swap by investigating the cash flows of both legs.

        References
        ----------
        swap.cpp + ratehelpers.cpp
        """
        fixed_leg = legs[0]
        date = Cashflows.end_date(fixed_leg)
        for idx in range(1, len(legs)):
            date = max(date, Cashflows.end_date(legs[idx]))
        return date
