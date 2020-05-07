import datetime
import pytz


def epoch(year, month, day, hour=0, minute=0):
    return int(
        datetime.datetime(year, month, day, hour, minute)
        .replace(tzinfo=pytz.UTC)
        .timestamp()
        * 1000
    )
