import typing
import pytz
import os
import math

from datetime import datetime, timedelta

def get_window_days(days: int, prefix='', suffix='') -> typing.Generator[str, None, None]:
    tz = pytz.timezone(os.getenv('TIMEZONE', 'America/Los_Angeles'))
    today = datetime.now(tz)
    one_day = timedelta(days=1)

    if days == 0:
      yield ''.join((prefix, today.strftime('%Y/%m/%d'), suffix))
    else:
      for i in range(days):
        calc_date = today - one_day * i
        yield ''.join((prefix, calc_date.strftime('%Y/%m/%d'), suffix))

def minutes_to_hour_minutes(minutes: int) -> str:
    hours = math.floor(minutes / 60)
    minutes = minutes % 60

    if hours == 0:
        msg = ""
    elif hours == 1:
        msg = f"{hours} hour"
    else:
        msg = f"{hours} hours"

    if minutes == 0:
        pass
    elif minutes == 1:
        msg += f" {minutes} minute"
    else:
        msg += f" {minutes} minutes"

    return msg


    return hours, minutes