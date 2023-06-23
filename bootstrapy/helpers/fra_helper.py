from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.calendars.calendar import advance, adjust
import datetime
from dateutil.rrule import rrule, MONTHLY, WE

# types
from typing import Callable


class FRAHelper(InterestRateHelper):
    def __init__(
        self,
        imm_offset_start: int,
        imm_offset_end: int,
        ibor_index: Callable,
        settlement_input: int,
        quote: float,
        pillar: str = "last_relevant_date",
        useIndexedCoupon: bool = True,
    ):
        self.imm_offset_start = imm_offset_start
        self.imm_offset_end = imm_offset_end
        self.fixing_days = settlement_input
        self.convention = ibor_index.convention
        self.day_count = ibor_index.day_count
        # New implementation of calendar dates
        self.reference_date = None
        self.earliest_date = None
        self.spot_date = None
        self.fixing_date = None
        self.maturity_date = None
        self.last_relevant_date = None
        self.pillar = pillar
        self.pillar_date = None
        self.value_date = None
        self.useIndexedCoupon = useIndexedCoupon
        self.ibor_index = ibor_index
        self.latest_relevant_date = None
        self.initialize_dates()
        self.maturity_days = maturity_int(
            reference_date_holder.reference_date, self.maturity_date
        )
        self.quote = quote

    def next_IMM_date(self, date: datetime.date) -> datetime.date:
        """
        Calculates the next IMM date given a date. Note the datetime.timedelta(days=1) is used in such a way that the if the current
        date is an imm date it will skip it.

        References
        ----------

        Parameters
        ----------

        """
        return list(
            rrule(
                MONTHLY,
                count=1,
                bymonth=[3, 6, 9, 12],
                byweekday=WE(3),
                dtstart=date + datetime.timedelta(days=1),
            )
        )[0].date()

    def nth_IMM_date(self, date: datetime.date, offset: int) -> datetime.date:
        """
        Calculates the imm date for a given date and offset n.

        References
        ----------
        ratehelpers.cpp

        """
        imm = date
        for i in range(offset):
            imm = self.next_IMM_date(imm)
        return imm

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
        self.spot_date = advance(
            self.reference_date, self.fixing_days, "D", self.convention
        )
        self.earliest_date = adjust(
            self.nth_IMM_date(self.spot_date, self.imm_offset_start), self.convention
        )

        self.maturity_date = adjust(
            self.nth_IMM_date(self.spot_date, self.imm_offset_end), self.convention
        )

        self.fixing_date = self.ibor_index.fixing_date(self.earliest_date)

        if self.useIndexedCoupon == True:
            self.latest_relevant_date = self.ibor_index.maturity_date(self.earliest_date)

        if self.pillar == "last_relevant_date":
            self.pillar_date = self.latest_relevant_date

    def implied_quote(self):
        raise NotImplementedError


#        return self.ibor_index.fixing(self.fixing_date)
