from typing import Union, Callable
import datetime
from abc import abstractmethod
import math


class InterestRate:
    def __init__(
        self,
        rate: Union[float, int],
        day_count: Callable,
        compounding: str,
        frequency: Callable,
    ):
        self.rate = rate
        self.day_count = day_count
        self.compounding = compounding
        self.frequency = frequency

    def __len__(self):
        raise NotImplementedError

    def year_fraction(
        self,
        accrual_start_date,
        accrual_end_date,
    ) -> Union[float, int]:
        """
        ref_period_start and ref_period_end could be removed as they are not used. However, they exists as arguments in QuantLib.
        """
        return self.day_count(accrual_start_date, accrual_end_date)

    def compound_factor(self, time: datetime.date) -> Union[float, int]:
        """
        Calculates the compounding factor given just a date.
        """
        if (self.compounding is None) or (self.compounding not in ["Simple"]):
            raise ValueError("Compounding")
        match self.compounding:
            case "Simple":
                return 1.0 + self.rate * time
            case "Continuous":
                return math.exp(self.rate * time)

    def compound_factor_accrual(
        self,
        accrual_start_date: datetime.date,
        accrual_end_date: datetime.date,
    ):
        """
        Calculates the compounding factor given the accrual start and end date.
        """
        time = self.year_fraction(
            accrual_start_date,
            accrual_end_date,
        )
        return self.compound_factor(time)
