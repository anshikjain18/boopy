from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import initialize_maturity_date, maturity_datetime, maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder

# types
from typing import Callable
class DepositHelper(InterestRateHelper):
    def __init__(self, maturity_input : str, settlement_input: int, daycounter: Callable[[int, int], float]):
        self.timeunit = maturity_input[-1]
        self.length = int(maturity_input[:len(maturity_input)-1])
        self.maturity_date = maturity_datetime(
            initialize_maturity_date(reference_date_holder.reference_date, self.timeunit, self.length),
            settlement_input 
            )
        self.maturity_days = maturity_int(reference_date_holder.reference_date, self.maturity_date)
        self.settlement_date = maturity_datetime(
            initialize_maturity_date(reference_date_holder.reference_date, "D", 
                                    settlement_input),
                                    settlement_input)
        self.settlement_days = maturity_int(reference_date_holder.reference_date, self.settlement_date)
        self.daycount_time = daycounter(self.settlement_days, self.maturity_days)

        self.value_date = None # Should be given by advancing the calendar.
    
    def implied_quote(self):
        raise NotImplementedError