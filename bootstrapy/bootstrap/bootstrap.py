from typing import List, Type, Callable
from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
from bootstrapy.time.date.maturity import time_from_reference
from bisect import bisect_right
import datetime
import numpy as np
from scipy import optimize
from functools import partial
class Bootstrap:
    def __init__(self, 
                 instruments : List[Type[InterestRateHelper]], 
                 day_counter : Callable[[int, int], float]
                 ):
        self.instruments = instruments
        self.day_counter = day_counter
        self.pillars = self._curve_pillars(instruments)

        self.curve = [-1, -1, -1]#len(self.pillars) * [0.5]

        # Interpolation
        self.x_begin = self.pillars
        self.x_end = self.pillars[-1]
        self.y_begin = self.curve
        # TODO: Temporary solution
        self.s_ = (len(self.curve ) +1)* [0]
    def _discount(self, 
                 d : datetime.time
                 ) -> float:
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
        print(f'{r = }')
        return np.exp(-r*t)
    
    # TODO: create a better solution for forecast_fixing, should be inside deposit_helper
    def _forecast_fixing(
            self,
            d1: datetime.date, 
            d2: datetime.date,
            t: float
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
            df_1 = self._discount(d1)
            df_2 = self._discount(d2)
            return (df_1/df_2-1)/t

    def _curve_pillars(self, 
                       instruments : List[Type[InterestRateHelper]]
                       ) -> List[int]:
        """
        Fetches the maturity days of the instruments and also inserts the reference date into a list. 
        
        Parameters
        ----------
        instruments : List[Type[InterestRateHelper]] 
            A list of class instances of the instruments.

        """
        pillars = [0] * (len(instruments) + 1)
        pillars[0] = 0 # Consider the reference date
        for i, instrument in enumerate(instruments):
            i += 1
            pillars[i] = self.day_counter(pillars[0],instrument.maturity_days)
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
        length = len(self.x_begin) - 1#len(self.x_end)
        for i in range(1,length):
            dx = self.x_begin[i] - self.x_begin[i-1]
            self.s_[i-1] = (self.y_begin[i] - self.y_begin[i-1]) / dx
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
        index_end = bisect_right(self.pillars, x)+1                                                                                             
        #x_ahead_end = self.pillars[index_end -1]
        x_begin = self.x_begin[0]
        if (x < x_begin):
            return 0
        #elif (x > x_ahead_end):
        #    raise NotImplementedError
        #    return self.x_end-self.x_begin-2
        else:
            # https://stackoverflow.com/a/37873955
            return bisect_right(self.pillars, x) - x_begin-1
    def bootstrap_error(self, 
                        r : float,
                        instrument : Callable,
                        segment: int, 
                        value_date: datetime.date,
                        maturity_date: datetime.date,
                        t : float
                        ) -> float:
            self.curve[segment] = r
            self.y_begin = self.curve
            if segment == 1:
                 self.curve[0] = self.curve[segment]
            print(f'{self._forecast_fixing(value_date, maturity_date, t) = }')
            return instrument.quote - self._forecast_fixing(value_date, maturity_date, t)
    def calculate_single(self):
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

        Parameters
        ----------
        
        """
        # ? Replace below with a for loop
        segment = 1 # ! consider the zero rate to be equal to the zero rate at element 1
        instrument = self.instruments[segment-1]
        value_date = instrument.value_date
        maturity_date = instrument.maturity_date
        t = instrument.year_fraction(value_date, maturity_date)
        self._update()

        pre_solve = partial(self.bootstrap_error,
                            instrument = instrument,
                            segment = segment,
                            value_date = value_date,
                            maturity_date = maturity_date,
                            t = t)
        optimize.root_scalar(lambda r: pre_solve(r = r), bracket=[-10, 10], method='brentq')
        return self.curve
    
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
        # ? Replace below with a for loop
        for segment in range(1,len(self.instruments)+1):
            print(f'{segment = }')
            instrument = self.instruments[segment-1]
            value_date = instrument.value_date
            maturity_date = instrument.maturity_date
            print(f'{value_date = }')
            print(f'{maturity_date = }')
            t = instrument.year_fraction(value_date, maturity_date)
            self._update()

            pre_solve = partial(self.bootstrap_error,
                                instrument = instrument,
                                segment = segment,
                                value_date = value_date,
                                maturity_date = maturity_date,
                                t = t)
            optimize.root_scalar(lambda r: pre_solve(r = r), bracket=[-1, 1], method='brentq')
        return self.curve
    def _order_instruments(self):
        """
        Orders the given instrument list of classes based on their maturity days.
        
        Parameters
        ----------
        instruments : List[Type[InterestRateHelper]] 
            A list of class instances of the instruments.

        """
        
        pass 