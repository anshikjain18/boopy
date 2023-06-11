import datetime
from dateutil.relativedelta import relativedelta
def is_weekend(arg_date : datetime.date) -> bool:
    """
    Returns true if date such as date(2023,1,2) is a weekend else false

    arg_date : date
        is a date object such as date(2023,1,2)
    """
    if arg_date.weekday() < 5:
        return False
    else:
        return True

def calc_day_of_year(arg_date : datetime.date) -> int:
    """
    Calculates the day of the year. For example datetime.date(2023,1,1) would be day of the year 1.

    arg_date : datetime.date
        The date of which to calculate the day of year.
    """
    return (arg_date- datetime.date(arg_date.year, 1, 1)).days + 1

def add_fixing(date: datetime.date, fixing: int, time_unit : str) -> datetime.date:
    """
    Corresponds to d + n*unit in calendar.cpp.

    References
    ----------
    calendar.cpp 
    """
    if time_unit == 'D' or time_unit =='d':
        return date + relativedelta(days=fixing)
    elif time_unit == 'W' or time_unit =='w':
        return date + relativedelta(weeks=fixing)
    elif time_unit == 'M' or time_unit =='m':
        return date + relativedelta(months=fixing)
    elif time_unit == 'Y' or time_unit =='y':
        return date + relativedelta(years=fixing)


if __name__ == "__main__":
    
    assert is_weekend(datetime.date(2023,4,2)) == True
    assert is_weekend(datetime.date(2023,4,1)) == True
    assert is_weekend(datetime.date(2023,4,3)) == False
    assert is_weekend(datetime.date(2023,4,4)) == False
    assert is_weekend(datetime.date(2023,4,5)) == False
    assert is_weekend(datetime.date(2023,4,6)) == False
    assert is_weekend(datetime.date(2023,4,7)) == False


    assert calc_day_of_year(datetime.date(2023,2,2)) == 33
    assert calc_day_of_year(datetime.date(2023,1,1)) == 1
    assert calc_day_of_year(datetime.date(2023,1,2)) == 2
    assert calc_day_of_year(datetime.date(2023,1,5)) == 5
