import typing
import pytz
import os

from datetime import datetime, timedelta

def get_window_days(days: int) -> typing.Generator[str, None, None]:
    tz = pytz.timezone(os.getenv('TIMEZONE', 'America/Los_Angeles')
    today = datetime.now(tz)
    one_day = timedelta(days=1)

    for i in range(days):
        calc_date = today - one_day * i
        yield calc_date.strftime('%Y/%m/%d')
