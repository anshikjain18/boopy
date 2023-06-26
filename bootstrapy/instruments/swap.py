import datetime

from typing import Callable


class Swap:
    def __init__(self):
        raise NotImplementedError

    def start_date(self) -> datetime.date:
        raise NotImplementedError

    def maturity_date(self) -> datetime.date:
        raise NotImplementedError
