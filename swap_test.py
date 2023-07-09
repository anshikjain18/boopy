from bootstrapy.time.schedule import Schedule
import datetime

start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)
tenor = "6M"
Schedule(
    start_date,
    end_date,
    tenor,
    "tempcalendar",
    "Following",
    "Following",
    "backward",
    "False",
)
