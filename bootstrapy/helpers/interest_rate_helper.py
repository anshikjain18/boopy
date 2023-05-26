import datetime
from typing import Callable



class InterestRateHelper:
    def __init__(
        self, 
        quote: float,
        day_count : Callable[[int, int], float]
    ):
        self.quote = quote
        self.day_count = day_count
    
    def year_fraction(self, d1 : datetime.date | None, d2: datetime.date) -> float:
        """
        Calculates the year fraction
        
        Parameters
        ----------

        """
        if d1 == None:
            d1 = 0
            return self.day_count(0, d2)
        else :
            return self.day_count(d1,d2)
            
        return 

