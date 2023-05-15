from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import initialize_maturity_date, maturity_datetime, maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance
# types
from typing import Callable
class DepositHelper(InterestRateHelper):
    def __init__(self, 
                 maturity_input : str, 
                 settlement_input: int, 
                 daycounter: Callable[[int, int], float]
                 ):
        self.timeunit = maturity_input[-1]
        self.length = int(maturity_input[:len(maturity_input)-1])
        self.maturity_date = maturity_datetime(
            initialize_maturity_date(reference_date_holder.reference_date, self.timeunit, self.length),
            settlement_input 
            )
        self.maturity_days = maturity_int(reference_date_holder.reference_date, self.maturity_date)

        self.value_date = advance(reference_date_holder.reference_date, settlement_input, "D", None)# Should be given by advancing the calendar.
        self.value_days = maturity_int(reference_date_holder.reference_date, self.value_date)
        # ? Should just be inserted to the function implied quote
        #self.daycount_time = daycounter(self.value_days, self.maturity_days)
    def implied_quote(self):
        raise NotImplementedError

