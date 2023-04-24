from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import initialize_maturity_date, maturity_datetime, maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
class DepositHelper(InterestRateHelper):
    def __init__(self, maturity_input : str, settlement_date: int):
        self.timeunit = maturity_input[-1]
        self.length = int(maturity_input[:len(maturity_input)-1])
        self.maturity_date = maturity_datetime(
            initialize_maturity_date(reference_date_holder.reference_date, self.timeunit, self.length),
            settlement_date
            )
        self.maturity_days =  maturity_int(reference_date_holder.reference_date, self.maturity_date)

        
