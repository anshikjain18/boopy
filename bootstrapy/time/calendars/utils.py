import datetime
from dateutil.relativedelta import relativedelta
from typing import Tuple


def is_weekend(arg_date: datetime.date) -> bool:
    """
    Returns true if date such as date(2023,1,2) is a weekend else false

    arg_date : date
        is a date object such as date(2023,1,2)
    """
    if arg_date.weekday() < 5:
        return False
    else:
        return True


def calc_day_of_year(arg_date: datetime.date) -> int:
    """
    Calculates the day of the year. For example datetime.date(2023,1,1) would be day of the year 1.

    arg_date : datetime.date
        The date of which to calculate the day of year.
    """
    return (arg_date - datetime.date(arg_date.year, 1, 1)).days + 1


def add_fixing(date: datetime.date, fixing: int, time_unit: str) -> datetime.date:
    """
    Corresponds to d + n*unit in calendar.cpp.

    References
    ----------
    calendar.cpp
    """
    if time_unit == "D" or time_unit == "d":
        return date + relativedelta(days=fixing)
    elif time_unit == "W" or time_unit == "w":
        return date + relativedelta(weeks=fixing)
    elif time_unit == "M" or time_unit == "m":
        return date + relativedelta(months=fixing)
    elif time_unit == "Y" or time_unit == "y":
        return date + relativedelta(years=fixing)


def is_period(period: str) -> bool:
    """
    Corresponds to d + n*unit in calendar.cpp.

    References
    ----------
    calendar.cpp
    """

    period = period[-1]
    if period == "D" or period == "d":
        return True
    elif period == "W" or period == "w":
        return True
    elif period == "M" or period == "m":
        return True
    elif period == "Y" or period == "y":
        return True
    else:
        return False


def convert_period(period: str) -> Tuple[int, str]:
    timeunit = period[-1]
    length = int(period[: len(period) - 1])
    return (length, timeunit)


def subtract_period(date: datetime.date, period: str) -> datetime.date:
    """
    In many cases we want to add the two values datetime.datetime(2023,2,4) and "3M" for example. Then
    we can call this function for that.
    """
    print(period)
    if period == "0D":
        return date
    else:
        time_unit = period[-1]
        length = int(period[: len(period) - 1])
        if time_unit == "D" or time_unit == "d":
            return date - relativedelta(days=length)
        elif time_unit == "W" or time_unit == "w":
            return date - relativedelta(weeks=length)
        elif time_unit == "M" or time_unit == "m":
            return date - relativedelta(months=length)
        elif time_unit == "Y" or time_unit == "y":
            return date - relativedelta(years=length)
        return date


def add_period(date: datetime.date, period: str) -> datetime.date:
    """
    In many cases we want to add the two values datetime.datetime(2023,2,4) and "3M" for example. Then
    we can call this function for that.
    """
    if period == "0D":
        return date
    else:
        time_unit = period[-1]
        length = int(period[: len(period) - 1])
        if time_unit == "D" or time_unit == "d":
            return date + relativedelta(days=length)
        elif time_unit == "W" or time_unit == "w":
            return date + relativedelta(weeks=length)
        elif time_unit == "M" or time_unit == "m":
            return date + relativedelta(months=length)
        elif time_unit == "Y" or time_unit == "y":
            return date + relativedelta(years=length)
        return date


def multiply_period(number: int, period: str):
    time_unit = period[-1]
    length = int(period[: len(period) - 1])
    new_length = number * length
    return str(new_length) + str(time_unit)


def year_fraction(d1: datetime.date | None, d2: datetime.date) -> float:
    """
    Calculates the year fraction. If d1 is equal to d1, then assume it will be the
    year fraction using the reference date.

    """

    if d1 == None:
        d1 = 0
        d2_int = time_from_reference(None, d2)
        return self.day_count(0, d2_int)
    else:
        d1_int = time_from_reference(None, d1)
        d2_int = time_from_reference(None, d2)
        return self.day_count(d1_int, d2_int)


def str_to_datetime(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def datetime_to_str(date: str) -> str:
    return date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    assert is_weekend(datetime.date(2023, 4, 2)) == True
    assert is_weekend(datetime.date(2023, 4, 1)) == True
    assert is_weekend(datetime.date(2023, 4, 3)) == False
    assert is_weekend(datetime.date(2023, 4, 4)) == False
    assert is_weekend(datetime.date(2023, 4, 5)) == False
    assert is_weekend(datetime.date(2023, 4, 6)) == False
    assert is_weekend(datetime.date(2023, 4, 7)) == False

    assert calc_day_of_year(datetime.date(2023, 2, 2)) == 33
    assert calc_day_of_year(datetime.date(2023, 1, 1)) == 1
    assert calc_day_of_year(datetime.date(2023, 1, 2)) == 2
    assert calc_day_of_year(datetime.date(2023, 1, 5)) == 5
