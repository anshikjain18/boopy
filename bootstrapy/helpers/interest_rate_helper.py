class InterestRateHelper:
    def __init__(
        self, 
        maturity : str, # Convert to string
        compounding : str, 
        rate: float,
        daycount: str):

        self.maturity = maturity
        self.compounding = compounding
        self.rate = rate
        self.daycount = daycount