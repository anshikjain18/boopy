from bootstrapy.time.calendars.sweden import sweden_is_business_day
import datetime
from dateutil.relativedelta import relativedelta
import bootstrapy.time.date.reference_date as reference_date_holder


def initialize_maturity_date(
    reference_date: datetime.date, timeunit: str, length: int
) -> datetime.date:
    """
    Calculates the maturity date without considering if the maturity date is a business date or not.

    Parameters
    ----------
    reference_date : datetime.date
        Corresponds to the date of which the bootstrap begins.

    timeunit : str
        Is the timeunit of the input, such as day, month or year.

    length : int
        Is the length of the timeunit, such as 10, if the input was 10D.
    """
    try:
        if (timeunit == "d") | (timeunit == "D"):
            return reference_date + datetime.timedelta(days=length)
        elif (timeunit == "m") | (timeunit == "M"):
            return reference_date + relativedelta(months=length)
        elif (timeunit == "y") | (timeunit == "Y"):
            return reference_date + relativedelta(years=length)
        else:
            raise TypeError("Timeunit or length is wrongly set.")
    except:
        raise TypeError("Timeunit or length is wrongly set.")


def maturity_datetime(
    init_maturity_date: datetime.date, settlement_days: int
) -> datetime.date:
    """
    Given init_maturity date which is the maturity date not considering if it is a business date or not,
    maturity_date will find the correct
    """

    # Interest rate is not accrued the day of the purchased
    maturity_date_iter = init_maturity_date + datetime.timedelta(days=1)
    boolean = True
    settlement_day_iter = 0
    while boolean == True:
        if sweden_is_business_day(maturity_date_iter) == True:
            settlement_day_iter += 1
            if settlement_day_iter == settlement_days:
                return maturity_date_iter

        maturity_date_iter = maturity_date_iter + datetime.timedelta(days=1)


def maturity_int(reference_date: datetime.date, maturity_date: datetime.date) -> int:
    return (maturity_date - reference_date).days


def time_from_reference(d1: datetime.date | None, d2: datetime.date) -> int:
    if d1 == None:
        return (d2 - reference_date_holder.reference_date).days
    else:
        return (d2 - d1).days
