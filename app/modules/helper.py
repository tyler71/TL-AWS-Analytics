import math
import os
import typing
from datetime import datetime, timedelta

import pandas as pd
import pytz
from modules import model


def get_window_days(days: int, prefix='', suffix='', start_date=None) -> typing.Generator[str, None, None]:
    tz = pytz.timezone(os.getenv('TZ', 'America/Los_Angeles'))
    if start_date is not None:
        today = start_date
    else:
        today = datetime.now(tz)
    one_day = timedelta(days=1)

    if days == 0:
        yield ''.join((prefix, today.strftime('%Y/%m/%d'), suffix))
    else:
        for i in range(days + 1):
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


# Specifically only get todays rows
def filter_today(df: pd.DataFrame, start_date=None) -> pd.DataFrame:
    tz = pytz.timezone(os.getenv('TZ', 'America/Los_Angeles'))
    ts = model.INITTIMESTAMP
    if start_date is not None:
        today = start_date
    else:
        today = datetime.now(tz)
    today = today.strftime('%Y/%m/%d')

    df['temp_date'] = pd.to_datetime(df[ts], format='%Y/%m/%d')
    df['temp_date'] = df['temp_date'].dt.tz_convert(tz)
    df = df.loc[(df['temp_date'] >= today)]

    df = df.drop('temp_date', axis=1)

    return df
