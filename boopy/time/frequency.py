from enum import Enum


class Frequency(Enum):
    """
    Enum to handle frequency which is realized in the period class.
    """

    ANNUAL = 1
    SEMIANNUAL = 2
    EVERYFOURMONTH = 3
    QUARTERLY = 4
    MONTHLY = 12
    DAILY = 365
