
from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance, adjust
# types
from typing import Callable
class FRAHelper(InterestRateHelper):
    def __init__(self, 
                 imm_offset_start: int,
                 imm_offset_end: int,
                 ibor_index: Callable,
                 settlement_input: int, 
                 quote: float):
        super().__init__(daycounter)
        self.timeunit = maturity_input[-1]
        self.length = int(maturity_input[:len(maturity_input)-1])
        self.fixing_days = settlement_input
        self.convention = convention
        # New implementation of calendar dates
        self.reference_date = None
        self.earliest_date = None
        self.fixing_date = None
        self.maturity_date = None
        self.pillar_date = None
        self.value_date = None
        self.initialize_dates()

        #? Move maturity_int to bootstrap function
        self.maturity_days = maturity_int(reference_date_holder.reference_date, self.maturity_date)
        self.value_days = maturity_int(reference_date_holder.reference_date, self.value_date)
        # ? Should just be inserted to the function implied quote
        self.quote = quote
    def initialize_dates(self):
        """
        Calculates the necessary dates for the deposits. 

        References
        ----------
        ratehelpers.cpp
        """
        self.reference_date = adjust(reference_date_holder.reference_date, self.convention)
        self.earliest_date = advance(self.reference_date,self.fixing_days, 'D', self.convention)
        self.fixing_date = advance(self.earliest_date,-self.fixing_days, 'D', self.convention)
        self.maturity_date = advance(self.earliest_date, self.length, self.timeunit, self.convention)
        self.pillar_date = self.maturity_date
        self.value_date = advance(self.fixing_date, self.fixing_days, "D", None)#
        

    def implied_quote(self):
        raise NotImplementedError
