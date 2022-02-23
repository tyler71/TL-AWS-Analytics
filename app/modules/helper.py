import typing
import pytz
import os
import math
import pandas as pd

from modules import model

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

# Specifically only get todays rows
def filter_today(df: pd.DataFrame) -> pd.DataFrame:
    tz = pytz.timezone(os.getenv('TIMEZONE', 'America/Los_Angeles'))
    ts = model.INITTIMESTAMP
    today = datetime.now(tz)
    today = today.strftime('%Y/%m/%d')

    df['temp_date'] = pd.to_datetime(df[ts], format='%Y/%m/%d')
    df['temp_date'] = df['temp_date'].dt.tz_convert(tz)
    df = df.loc[(df['temp_date'] == today)]
  
    df = df.drop('temp_date', axis=1)
  
    return df