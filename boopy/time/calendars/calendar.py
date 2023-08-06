from boopy.time.calendars.sweden import sweden_is_business_day
from boopy.time.calendars.null_calendar import null_calendar
from boopy.time.calendars.utils import add_fixing, multiply_period
import datetime


def adjust(date: datetime.date, convention: str, null: bool = False):
    """
    Adjusts a given non business day to the next business day with respect to a convention. Note here we replace isHoliday with
    calendar. In the future this will be reimplemented.

    Parameters
    ----------

    Date : str
        The date to make the evaluation, for deposits it should be the reference date.
    convention : str
        The business day convention, such as following, modified following and such.
    """
    # Quick fix to create a null calendar for schedule.
    calendar = sweden_is_business_day

    if null == True:
        calendar = null_calendar

    if convention == "unadjusted":
        return date

    date1 = date
    if (
        convention == "Following"
        or convention == "ModifiedFollowing"
        or convention == "HalfMonthModifiedFollowing"
    ):
        while calendar(date1) == False:
            date1 = date1 + datetime.timedelta(days=1)
        if (
            convention == "ModifiedFollowing"
            or convention == "HalfMonthModifiedFollowing"
        ):
            if date1.month != date.month:
                return adjust(date, "Preceding")
            if convention == "HalfMonthModifiedFollowing":
                if date.day <= 15 and date1.day > 15:
                    return adjust(date, "Preceding")

    elif convention == "Preceding" or convention == "ModifiedPreceding":
        while calendar(date1) != True:
            date1 = date1 - datetime.timedelta(days=1)
        if convention == "ModifiedPreceding" and (date1.month != date.month):
            return adjust(date, "Following")
    elif convention == "Nearest":
        date2 = date
        while (calendar(date1) != True) and (calendar(date2) != True):
            date1 = date1 + datetime.timedelta(days=1)
            date2 = date2 - datetime.timedelta(days=1)
        if calendar(date1) != True:
            return date2
        else:
            return date1
    else:
        raise ValueError("Unknown business-day convention")
    return date1


def advance(
    date: datetime.date, n: int, time_unit: str, convention: str, null: bool = False
):
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
    # Quick fix to create a null calendar for schedule.
    calendar = sweden_is_business_day

    if null == True:
        calendar = null_calendar
    if n == 0:
        return adjust(date, convention)
    elif (time_unit == "D") | (time_unit == "d"):
        d1 = date
        if n > 0:
            while n > 0:
                d1 = d1 + datetime.timedelta(days=1)
                while calendar(d1) != True:
                    d1 = d1 + datetime.timedelta(days=1)
                n -= 1
        else:
            while n < 0:
                d1 = d1 + datetime.timedelta(days=-1)
                while calendar(d1) != True:
                    d1 = d1 + datetime.timedelta(days=-1)
                n += 1
        return d1
    # To be implemented calendar.cpp
    elif time_unit == "W" or time_unit == "w":
        d1 = add_fixing(date, n, time_unit)  # What is time_unit
        return adjust(d1, convention)
    else:
        d1 = add_fixing(date, n, time_unit)  # n * time_unit  # What is time_unit
        return adjust(d1, convention, null)
