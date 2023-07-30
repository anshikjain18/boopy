import datetime


def ACT360(t1: int, t2: int) -> float:
    if isinstance(t1, datetime.date) and isinstance(t2, datetime.date):
        return (t2 - t1).days / 360
    return (t2 - t1) / 360


def ACT365(t1: int, t2: int) -> float:
    return (t2 - t1) / 365
