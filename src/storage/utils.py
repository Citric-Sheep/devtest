from datetime import datetime


def datetime_to_integer(dt: datetime) -> int:
    """
    Convert a datetime object to an integer representation (HHMM).

    Args:
        dt (datetime): The datetime object to be converted.

    Returns:
        int: An integer representation of the time in the format HHMM.
    """
    return dt.hour * 100 + dt.minute
