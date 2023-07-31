import datetime
from typing import Callable, Union
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.utils import convert_period, multiply_period
from bootstrapy.time.calendars.calendar import advance, adjust


class Schedule:
    def __init__(
        self,
        effective_date: datetime.datetime,
        termination_date: datetime.datetime,
        tenor: str,
        calendar: Callable,
        convention: Callable,
        termination_date_convention: Callable,
        rule: str,
        end_of_month: bool = False,
        first_date: Union[datetime.datetime, None] = None,
        next_to_last: Union[datetime.datetime, None] = None,
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
        self.is_regular = []
        self.initialize_dates()

    def has_tenor(self):
        return self.tenor != None

    def has_is_regular(self):
        return len(self.is_regular) != 0

    def __len__(self):
        return len(self.dates)

    def initialize_dates(self) -> None:
        """
        Should be moved to __init__. A function to generate the coupons dates.
        References
        ----------

        Parameters
        ----------

        """
        if (
            (self.effective_date == None)
            & (self.first_date == None)
            & (self.first_date == "backward")
        ):
            eval_date = reference_date_holder.reference_date
            if self.next_to_last != None:
                raise NotImplementedError
            else:
                raise NotImplementedError
        tenor_length, tenor_unit = convert_period(self.tenor)

        if tenor_length == 0:
            self.rule = "zero"
        # else:
        #    raise ValueError("Accrued payments for coupons can not be zero days")

        if self.first_date != None:
            raise NotImplementedError

        if self.next_to_last != None:
            raise NotImplementedError

        match self.rule:
            case "zero":
                raise NotImplementedError
            case "backward":
                """
                Add explanation
                """
                # add termination date to the end of the list
                self.dates.append(self.termination_date)
                seed = self.termination_date
                periods = 1

                """
                Add explanation 
                """
                if self.next_to_last != None:
                    raise NotImplementedError
                exit_date = self.effective_date

                """
                Add explanation 
                """
                if self.first_date != None:
                    exit_date = self.first_date
                while True:
                    new_tenor = multiply_period(periods, self.tenor)
                    tenor_length, tenor_unit = convert_period(new_tenor)
                    temp = advance(
                        seed, -tenor_length, tenor_unit, self.convention, True
                    )
                    if temp < exit_date:
                        statement_1 = self.first_date != None
                        if statement_1 == True:
                            statement_2 = adjust(
                                self.dates[0], self.convention
                            ) != adjust(self.first_date, self.convention)
                            if statement_2 == True:
                                self.dates.insert(0, self.first_date)
                                self.is_regular.insert(0, False)
                        break
                    else:
                        if adjust(self.dates[0], self.convention) != adjust(
                            temp, self.convention
                        ):
                            self.dates.insert(0, temp)
                            self.is_regular.insert(0, True)
                        periods = periods + 1

                if adjust(self.dates[0], self.convention) != adjust(
                    self.effective_date, self.convention
                ):
                    self.dates.insert(0, self.effective_date)
                    self.is_regular.insert(0, False)
            case "forward":
                raise NotImplementedError

            # Adjustments
            # Implement end of month logic
        if self.end_of_month == True:
            raise NotImplementedError
        else:
            if self.rule != "old_cds":
                self.dates[0] = adjust(self.dates[0], self.convention)
            for i in range(1, len(self.dates) - 1):
                self.dates[i] = adjust(self.dates[i], self.convention)
