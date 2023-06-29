import datetime

from typing import Callable


class Swap(object):
    def __init__(self):
        raise NotImplementedError

    def fixed_leg(self) -> None:
        """
        References
        ----------
        vanillaswap.cpp
        """
        raise NotImplementedError

    def ibor_leg(self) -> None:
        """
        References
        ----------
        vanillaswap.cpp
        """
        raise NotImplementedError

    def start_date(self) -> datetime.date:
        raise NotImplementedError

    def maturity_date(self) -> datetime.date:
        raise NotImplementedError
