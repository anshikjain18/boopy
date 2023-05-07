from bootstrapy.time.calendars.sweden import sweden_is_business_day
import datetime
def adjust(date : str,
           convention : str ):
    """
    Adjusts a given non business day to the next business day with respect to a convention

    Parameters
    ----------

    Date : str
        The date to make the evaluation, for deposits it should be the reference date.
    convention : str
        The business day convention, such as following, modified following and such.
    """
    pass
def advance(date : datetime.date,
            n : int,
            time_unit : str,
            convention : str):
    """
    Parameters
    ----------
    Date : str
        The date to make the evaluation, for deposits it should be the reference date.
    n : int
        The fixing days, for example a tomorrow next deposit has 2 days in Sweden.
    time_unit : str
        The time unit of   
    convention : str
        The business day convention, such as following, modified following and such.

    """
    if (n == 0):
        return adjust(date, convention)
    elif (time_unit == 'D') | (time_unit == 'd'):
        d1 = date
        if (n > 0):
            while (n > 0):
                d1 = d1 + datetime.timedelta(days=1)
                while (sweden_is_business_day(d1) != True):
                    d1 = d1 + datetime.timedelta(days=1)
                n -= 1
        else:
            while (n < 0):
                d1 = d1 + datetime.timedelta(days = -1)
                while (sweden_is_business_day(d1) != True):
                    d1 = d1 + datetime.timedelta(days = -1)
                n += 1
        return d1
    # To be implemented calendar.cpp
    #elif time_unit == 'W' | time_unit == 'w':
        #d1 = d + n *unit 

        