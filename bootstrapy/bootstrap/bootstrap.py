from typing import List, Type, Callable
from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
import bootstrapy.time.date.reference_date as reference_date_holder
from bisect import bisect_right
class Bootstrap:
    def __init__(self, 
                 instruments : List[Type[InterestRateHelper]], 
                 day_counter : Callable[[int, int], float]
                 ):
        self.day_counter = day_counter
        self.pillars = self._curve_pillars(instruments)
        self.x_begin = self.pillars[0]
        self.x_end = self.pillars[-1]
        self.curve = len(self.pillars) * [0.5]
    def _curve_pillars(self, instruments : List[Type[InterestRateHelper]]) -> List[int]:
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

    def _update(self, x_begin : List[float], x_end : float, y_begin : float):
        """
        Calculates the quota (y(x1)-y(x0)/(x1-x0)) a given point on the curve based on the interpolation method. 
        
        Reference
        ---------
        linearinterpolation.hpp

        Parameters
        ----------
        
        """
        pass
    
    def _value(self, x_begin : float, x_end : float, y_begin : float):
        pass

    def _locate(self, x: float) -> int:
        """
        Given a x, it will locate the correct index in the corresponding yBegin and x_begin arrays.
        
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
        x_ahead_end = self.pillars[index_end -1]
        if (x < self.x_begin):
            return 0
        elif (x > x_ahead_end):
            raise NotImplementedError
            #return self.x_end-self.x_begin-2
        else:
            # https://stackoverflow.com/a/37873955
            return bisect_right(self.pillars, x) - self.x_begin-1
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

        Parameters
        ----------
        
        """
    def _order_instruments(self):
        """
        Orders the given instrument list of classes based on their maturity days.
        
        Parameters
        ----------
        instruments : List[Type[InterestRateHelper]] 
            A list of class instances of the instruments.

        """
        pass 