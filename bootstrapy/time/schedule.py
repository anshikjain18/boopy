import datetime
from typing import Callable, Union
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.utils import convert_period


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
        first_date: Union[datetime.datetime, None],
        next_to_last: Union[datetime.datetime, None],
    ):
        self.effective_date = effective_date
        self.termination_date = termination_date
        self.tenor = tenor
        self.calendar = calendar
        self.convention = convention
        self.termination_date_convention = termination_date_convention
        self.rule = rule
        self.end_of_month = end_of_month
        self.first_date = first_date
        self.next_to_last = next_to_last
        self.dates = []
        self.initialize_dates()

    def initialize_dates(self) -> None:
        if (
            (self.effective_date == None)
            & (self.first == None)
            & (self.first == "backward")
        ):
            eval_date = reference_date_holder.reference_date
            if self.next_to_last != None:
                raise NotImplementedError
            else:
                raise NotImplementedError

        tenor_length, _ = convert_period(self.tenor)

        if tenor_length == 0:
            self.rule = "zero"
        else:
            raise ValueError("Accrued payments for coupons can not be zero days")

        if self.first_date != None:
            raise NotImplementedError

        if self.next_to_last != None:
            raise NotImplementedError

        match self.rule:
            case "zero":
                raise NotImplementedError
            case "backward":
                # add termination date to the end of the list
                self.dates.insert(len(self.dates), self.termination_date)
                seed = self.termination_date
                if self.next_to_last != None:
                    raise NotImplementedError
                exit_date = self.effective_date
                if self.first_date != None:
                    exit_date = self.first_date
                while True:
                    temp = c
            case "forward":
                raise NotImplementedError
