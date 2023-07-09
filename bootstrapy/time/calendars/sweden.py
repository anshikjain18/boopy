import datetime
from dateutil import easter # Only needed for Easter Monday
from bootstrapy.time.calendars.utils import is_weekend, calc_day_of_year

def sweden_is_business_day(arg_date : datetime.date) -> bool:
    weekday = arg_date.weekday()
    day_of_month = arg_date.day 
    day_of_year = (arg_date- datetime.date(arg_date.year, 1, 1)).days + 1
    month = arg_date.month
    year = arg_date.year
    easter_monday = calc_day_of_year(easter.easter(year,3) + datetime.timedelta(1))
    if (is_weekend(arg_date)
        # Good Friday
        | (day_of_year == easter_monday -3)
        # Easter Monday
        | (day_of_year == easter_monday) 
        # Ascension Thursday
        | (day_of_year == easter_monday+38)
        # Whit Monday (till 2004)
        | ((day_of_year == easter_monday + 49) & (year < 2005))
        # New Year's Day
        | ((day_of_month == 1) & (month == 1))
        # Epiphany
        | ((day_of_month == 6) & (month == 1))
        # May Day
        | ((day_of_month == 1) & (month == 5))
        # National Day
        # Only a holiday since 2005
        | ((day_of_month == 6) & (month == 6) & (year >= 2005))
        # Midsummer Eve (Friday between June 19-25)
        | ((weekday == 4 ) & (day_of_month >= 19) & (day_of_month <= 25) & (month == 6))
        # Christmas Eve
        | ((day_of_month == 24) & month == 12)
        # Christmas Day
        | ((day_of_month == 25) & (month ==12))
        # Boxing Day
        | ((day_of_month == 26) & (month ==12))
        # New Year's Eve
        | ((day_of_month == 31) & (month == 12))
        ):
        return False
    else:
        return True



if __name__ == '__main__':
    assert sweden_is_business_day(datetime.date(2023,1,6)) == False
    assert sweden_is_business_day(datetime.date(2023,4,2)) == False 
    assert sweden_is_business_day(datetime.date(2023,4,1)) == False 
    assert sweden_is_business_day(datetime.date(2023,4,3)) == True 
    assert sweden_is_business_day(datetime.date(2023,4,7)) == False   # Good Friday
    assert sweden_is_business_day(datetime.date(2023,4,10)) == False  # Easter Monday
    assert sweden_is_business_day(datetime.date(2023,5,18)) == False  # Ascension Thursday
    assert sweden_is_business_day(datetime.date(2023,5,18)) == False  # Whit Monday
    assert sweden_is_business_day(datetime.date(2023,1,1)) == False   # New Year's Day
    assert sweden_is_business_day(datetime.date(2023,1,6)) == False   # Epiphany
    assert sweden_is_business_day(datetime.date(2023,6,6)) == False   # National Day
    assert sweden_is_business_day(datetime.date(2023,6,24)) == False  # Midsummer Eve
    assert sweden_is_business_day(datetime.date(2023,12,24)) == False # Christmas Eve
    assert sweden_is_business_day(datetime.date(2023,12,25)) == False # Christmas Day
    assert sweden_is_business_day(datetime.date(2023,12,26)) == False  # Boxing Day
    assert sweden_is_business_day(datetime.date(2023,12,31)) == False  # New Year's Eve
