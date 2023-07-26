from typing import Union, List, Callable, Type
from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from scipy import optimize
from functools import partial
from bootstrapy.bootstrap.term_structure import TermStructure
from bootstrapy.time.date.maturity import maturity_int
import bootstrapy.time.date.reference_date as reference_date_holder
from bootstrapy.time.date.maturity import time_from_reference


class Bootstrap:
    def __init__(
        self,
        helpers: List[Type[InterestRateHelper]],
        day_counter: Callable[[int, int], float],
    ):
        self.helpers = helpers
        self.day_counter = day_counter
        self.maturity_days = [0]
        self.pillars = self._curve_pillars(helpers)
        self.term_structure = TermStructure(helpers, day_counter)
        self.boolean = True

    def _curve_pillars(self, instruments: List[Type[InterestRateHelper]]) -> List[int]:
        """
        Fetches the maturity days of the instruments and also inserts the reference date into a list.

        Parameters
        ----------
        instruments : List[Type[InterestRateHelper]]
            A list of class instances of the instruments.

        """
        pillars = [0] * (len(instruments) + 1)
        pillars[0] = 0  # Consider the reference date
        for i, instrument in enumerate(instruments):
            i += 1
            pillar = instrument.pillar_date
            maturity_days = maturity_int(reference_date_holder.reference_date, pillar)
            self.maturity_days.append(maturity_days)
            pillars[i] = self.day_counter(pillars[0], maturity_days)
        return pillars

    def bootstrap_error(
        self,
        r: float,
        helper: Callable,
        segment: int,
    ) -> float:
        self.term_structure.zero_curve[segment] = r
        if segment == 1:
            # the first rate is always equivalent to the second value in a zero rate curve
            self.term_structure.zero_curve[0] = self.term_structure.zero_curve[segment]

        self.term_structure._update()
        return helper.quote - helper.implied_quote(
            self.term_structure
        )  # self._forecast_fixing(value_date, maturity_date, t)

    def calculate(self):
        """
        When called will extend the curve pillar at a time with each new instrument.

        Example
        -------
        Given the first instrument, a deposit. It will extend the curve with a single point.
        Then for the next instrument, it will extend the curve with an additional point. Each
        instrument forces the curve to call the solver and interpolate again.

        Reference
        ---------
        iterativebootstrap.hpp
        """
        for segment in range(1, len(self.helpers) + 1):
            helper = self.helpers[segment - 1]
            self.initialize_interpolation(segment)

            partial_error = partial(
                self.bootstrap_error,
                helper=helper,
                segment=segment,
            )
            optimize.root_scalar(
                lambda r: partial_error(r=r), bracket=[-1, 1], method="brentq"
            )
        return (
            self.term_structure
        )  # self.term_structure.zero_curve temporary for implementating swap discounting

    def initialize_interpolation(self, segment: int) -> None:
        self.term_structure.x_begin = 0
        self.term_structure.x_end = self.term_structure.x_begin + segment + 1

        self.term_structure.x = self.pillars
        self.term_structure.y = self.term_structure.zero_curve
