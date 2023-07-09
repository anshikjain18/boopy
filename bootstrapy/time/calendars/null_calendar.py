from bootstrapy.time.calendars.utils import is_weekend
import datetime


def null_calendar(date: datetime.date) -> bool:
    """
    A null calendar to calculate dates for schedule. Contains no holidays but check for weekends.

    References
    ----------
    schedule.cpp
    nullcalendar.hpp
    """
    if is_weekend(date) == True:
        return False  # Not a business days
    else:
        return True
