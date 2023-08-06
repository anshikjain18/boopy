from typing import Union, List, Callable, Type
import datetime
import numpy as np
from bisect import bisect_right
from boopy.time.date.maturity import time_from_reference


class TermStructure:
    def __init__(self, helpers: Callable, day_counter: Callable):
        self.zero_curve = [0] * (len(helpers) + 1)
        self.day_counter = day_counter
        # Interpolation
        self.x_begin = None
        self.x_end = None
        self.x = None
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
        return self.y[i] + (x - self.x[i]) * self.s_[i]

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
        if x < self.x[self.x_begin]:
            return 0
        elif x > self.x[self.x_end - 1]:
            return self.x_end - self.x_begin - 2
        else:
            # https://stackoverflow.com/a/37873955
            return (
                bisect_right(self.x, x - 0.000000001) - self.x_begin - 1
            )  # 0.0000001 is to mimic c++ upper bound

    def _update(self) -> None:
        """
        Calculates the quota (y(x1)-y(x0)/(x1-x0)) a given point on the curve based on the interpolation method.

        Reference
        ---------
        linearinterpolation.hpp
        """
        for i in range(1, self.x_end - self.x_begin):
            dx = self.x[i] - self.x[i - 1]
            self.s_[i - 1] = (self.y[i] - self.y[i - 1]) / dx
