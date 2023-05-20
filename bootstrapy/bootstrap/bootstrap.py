from typing import List, Type
from bootstrapy.helpers.interest_rate_helper import InterestRateHelper
import bootstrapy.time.date.reference_date as reference_date_holder
class Bootstrap:
    def __init__(self, instruments : List[Type[InterestRateHelper]]):
        self.pillars = self._curve_pillars(instruments)
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
            pillars[i] = instrument.maturity_days
        return pillars

    def _update_interpolation(self, x_begin : float, x_end : float, y_begin : float):
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

    def _locate(self):
        pass

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