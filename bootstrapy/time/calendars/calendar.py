
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
def advance(date : str,
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
    pass