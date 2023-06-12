from typing import Callable
class IborIndex:
    def __init__(self, 
                 settlement_days : int,
                 period : str,
                 calendar : Callable,
                 convention : str,
                 day_count : Callable):
        self.settlement_days = settlement_days
        self.timeunit = period[-1]
        self.length = int(period[:len(period)-1])
        self.calendar = calendar
        self.convention = convention
        self.day_count = day_count