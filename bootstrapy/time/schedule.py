import datetime
from typing import Callable


class Schedule:
    def __init__(
        self,
        effective_date: datetime.datetime,
        termination_date: datetime.datetime,
        tenor: str,
        calendar: Callable,
        convention: Callable,
        termination_date_convention: Callable,
        rule,
        end_of_month: str,
        first: datetime.datetime,
        next_to_last: datetime.datetime,
    ):
        raise NotImplementedError
