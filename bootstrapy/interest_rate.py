from typing import Union, Callable
import datetime
from abc import abstractmethod


class InterestRate:
    def __init__(
        self,
        rate: Union[float, int],
        day_count: Callable,
        compounding: Callable,
        frequency: Callable,
    ):
        self.rate = rate
        self.day_count = day_count
        self.compounding = compounding
        self.frequency = frequency

    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def simple(rate: Union[float, int], t: Union[float, int]) -> float:
        return 1 + rate * t

    @abstractmethod
    def year_fraction(
        self,
        accrual_start_date,
        accrual_end_date,
        ref_period_start,
        ref_period_end,
        day_count,
    ) -> Union[float, int]:
        return day_count(accrual_start_date, accrual_end_date)

    @abstractmethod
    def compound_factor(
        rate: Union[float, int],
        accrual_start_date: datetime.date,
        accrual_end_date: datetime.date,
        day_count: Callable,
        ref_period_start: datetime.date = None,
        ref_period_end: datetime.date = None,
    ):
        time = InterestRate.year_fraction(
            accrual_start_date,
            accrual_end_date,
            ref_period_start,
            ref_period_end,
            day_count,
        )
