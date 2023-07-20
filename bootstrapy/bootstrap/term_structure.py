from typing import Union, List, Callable, Type
import datetime
from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
import numpy as np
from scipy import optimize
from functools import partial
from bisect import bisect_right

from bootstrapy.time.date.maturity import time_from_reference


class TermStructure:
    def __init__(self, helpers: Callable, day_counter: Callable):
        self.zero_curve = [0] * (len(helpers) + 1)
        self.day_counter = day_counter
        self.pillars = self._curve_pillars(helpers)
        # Interpolation
        self.x_begin = self.pillars
        self.x_end = self.pillars[-1]
        self.y_begin = self.zero_curve
        self.s_ = (len(self.zero_curve) + 1) * [0]

    def _discount(self, d: datetime.time) -> float:
        """
        Considers jumpTimes and such. However, we will skip it for now and just call discountImpl directly.
        References
        ----------
        yieldtermstructure.cpp
        zeroyieldstructure.hpp

        Parameters
        ----------

        """
        t = self.day_counter(0, time_from_reference(None, d))
        r = self._value(t)
        return np.exp(-r * t)

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
            pillars[i] = self.day_counter(pillars[0], instrument.maturity_days)
        return pillars

    def _update(self) -> None:
        """
        Calculates the quota (y(x1)-y(x0)/(x1-x0)) a given point on the curve based on the interpolation method.

        Reference
        ---------
        linearinterpolation.hpp

        Parameters
        ----------

        """
        length = len(self.x_begin) - 1  # len(self.x_end)
        for i in range(1, length):
            dx = self.x_begin[i] - self.x_begin[i - 1]
            self.s_[i - 1] = (self.y_begin[i] - self.y_begin[i - 1]) / dx

    def _value(self, x: float):
        """
        Given a x it will locate the nearest pillar using the corresponding version of upper_bound in python which is
        left_bisect. Then it will use the curve value for that pillar to interpolate.

        Reference
        ---------
        linearinterpolation.hpp

        Parameters
        ----------
        x : float
            The pillar to find the interpolated value for, it can also be value date.
        """
        i = self._locate(x)
        return self.y_begin[i] + (x - self.x_begin[i]) * self.s_[i]

    def _locate(self, x: float) -> int:
        """
        Given a x, it will locate the correct index in the corresponding x_begin array.

        Example
        -------
        x_begin is always the start of the curve. x_end is always the next pillar of the curve of that instrument.
        Assume you have the following pillars: [0, 0.0136986301369863, 0.0958904,  0.25753424657534246]
        then for a given value date, assume 0.0109589, then x_end will be 0.0958904. Instead assume we have x is equal to one
        of the pillars then x_end will be that pillar.

        References
        ----------
        interpolation.hpp

        Parameters
        ----------
        x : float
            The pillar to find the interpolated value for.
        x_begin: float
            The initial pillar of the curve, is most likely 0.
        x_end: float
            The
        """
        index_end = bisect_right(self.pillars, x) + 1
        # x_ahead_end = self.pillars[index_end -1]
        x_begin = self.x_begin[0]
        if x < x_begin:
            return 0
        # elif (x > x_ahead_end):
        #    raise NotImplementedError
        #    return self.x_end-self.x_begin-2
        else:
            # https://stackoverflow.com/a/37873955
            return bisect_right(self.pillars, x) - x_begin - 1


class Bootstrap:
    def __init__(
        self,
        helpers: List[Type[InterestRateHelper]],
        day_counter: Callable[[int, int], float],
    ):
        self.helpers = helpers
        self.day_counter = day_counter
        self.term_structure = TermStructure(helpers, day_counter)

    def bootstrap_error(
        self,
        r: float,
        helper: Callable,
        segment: int,
        value_date: datetime.date,
        maturity_date: datetime.date,
        t: float,
    ) -> float:
        print(f"{self.term_structure.zero_curve = }")
        self.term_structure.zero_curve[segment] = r
        self.y_begin = self.term_structure.zero_curve
        if segment == 1:
            # the first rate is always equivalent to the second value in a zero rate curve
            self.term_structure.zero_curve[0] = self.term_structure.zero_curve[segment]
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
            value_date = helper.value_date
            maturity_date = helper.maturity_date
            t = helper.year_fraction(value_date, maturity_date)
            self.term_structure._update()

            partial_error = partial(
                self.bootstrap_error,
                helper=helper,
                segment=segment,
                value_date=value_date,
                maturity_date=maturity_date,
                t=t,
            )
            optimize.root_scalar(
                lambda r: partial_error(r=r), bracket=[-1, 1], method="brentq"
            )
        print(f"{self.term_structure.zero_curve = }")
        return self.term_structure.zero_curve
