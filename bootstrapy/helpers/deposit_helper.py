from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance, adjust

# types
from typing import Callable
import datetime


class DepositHelper(InterestRateHelper):
    def __init__(
        self,
        maturity_input: str,
        settlement_input: int,
        daycounter: Callable[[int, int], float],
        quote: float,
        convention: str,
    ):
        super().__init__(daycounter)
        self.timeunit = maturity_input[-1]
        self.length = int(maturity_input[: len(maturity_input) - 1])
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

        # ? Move maturity_int to bootstrap function
        self.maturity_days = maturity_int(
            reference_date_holder.reference_date, self.maturity_date
        )
        self.value_days = maturity_int(
            reference_date_holder.reference_date, self.value_date
        )
        # ? Should just be inserted to the function implied quote
        self.quote = quote

    def initialize_dates(self):
        """
        Calculates the necessary dates for the deposits.

        References
        ----------
        ratehelpers.cpp
        """
        self.reference_date = adjust(
            reference_date_holder.reference_date, self.convention
        )
        self.earliest_date = advance(
            self.reference_date, self.fixing_days, "D", self.convention
        )
        self.fixing_date = advance(
            self.earliest_date, -self.fixing_days, "D", self.convention
        )
        self.maturity_date = advance(
            self.earliest_date, self.length, self.timeunit, self.convention
        )
        self.pillar_date = self.maturity_date
        self.value_date = advance(self.fixing_date, self.fixing_days, "D", None)  #

    def _forecast_fixing(
        self, d1: datetime.date, d2: datetime.date, t: float, TermStructure: Callable
    ) -> float:
        """
        Calculates the forward rate using d1 and d2. t is the time between d1 and d2 using the instruments
        day count convention.

        References
        ----------
        Calls discountImpl which will return exp(-r*t). However first r is calculated through calling value from interpolation.
            iborindex.hpp

        Parameters
        ----------

        """

        df_1 = TermStructure._discount(d1)
        df_2 = TermStructure._discount(d2)
        return (df_1 / df_2 - 1) / t

    def implied_quote(self, TermStructure: Callable):
        """
        Calculates the implied quote given a term structure. In terms of bootstrap this means that we will
        guess the discount factors with a numerical solver as the forward rate converges to the market quote.
        """
        d1 = self.value_date
        d2 = self.maturity_date
        t = self.year_fraction(d1, d2)
        return self._forecast_fixing(d1, d2, t, TermStructure)
