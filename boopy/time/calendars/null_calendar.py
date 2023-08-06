from boopy.time.calendars.utils import is_weekend
import datetime


def null_calendar(date: datetime.date) -> bool:
    """
    A null calendar to calculate dates for schedule. Contains no holidays but check for weekends.
    Thus, if it is a business day it should return True else False
    References
    ----------
    schedule.cpp
    nullcalendar.hpp
    """
    if is_weekend(date) == True:
        return False  # Not a business days
    else:
        return True
