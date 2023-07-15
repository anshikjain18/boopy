from typing import Union, Callable
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
