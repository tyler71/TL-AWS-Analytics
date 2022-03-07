import math
import os
import typing
from datetime import datetime, timedelta
import functools
import streamlit as st

import pytz


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


def minute_to_hour_minute_second(seconds=None, minutes=None, hours=None) -> str:
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

def time_to_hour_minute_second(hours=0, minutes=0, seconds=0) -> str:
  delta_seconds = timedelta(seconds=seconds)
  delta_minutes = timedelta(minutes=minutes)
  delta_hours   = timedelta(hours=hours)
  set_time = delta_seconds + delta_minutes + delta_hours
  return set_time.__str__()

def sha():
    sha = os.getenv("GIT_SHA", "dev")
    git_url = os.getenv("GIT_COMMIT_URL", "https://github.com/tyler71/TL-AWS-Analytics/commit")
    sha_msg = f"*[{sha[:6]}]({git_url}/{sha})*"
    return sha_msg

def show_empty_dec(func):
  # Writes out "No data available" if it is empty
  # after output
  @functools.wraps(func)
  def report_if_empty(*args, **kwargs):
    output = func(*args, **kwargs)
    if output.empty:
      st.info("No data available")
      st.stop()
    return output
  return report_if_empty