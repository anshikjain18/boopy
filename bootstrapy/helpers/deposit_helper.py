class DepositHelper:
    def __init__(
        self, 
        maturity : int, # Convert to string
        compounding : str, 
        rate: float,
        daycount: str):

        self.maturity = maturity
        self.compounding = compounding
        self.rate = rate
        self.daycount = daycount

    def rate(self):
        if self.compounding == "Continuous":
            raise NotImplementedError
        elif self.compounding == "Annual": # Consider discrete compounding instead
            raise NotImplementedError
        elif self.compounding == "Simple":
            raise NotImplementedError
        else:
            raise TypeError("Deposit compounding is not set correctly.")
        
    def continuous_rate(self):
        raise NotImplementedError
    
    def simple_rate(self):
        raise NotImplementedError
    
    def discrete_compounding(self):
        raise NotImplementedError