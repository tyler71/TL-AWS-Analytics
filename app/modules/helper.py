import math
import os
import typing
from datetime import datetime, timedelta

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


def sha():
    sha = os.getenv("GIT_SHA", "dev")
    git_url = os.getenv("GIT_COMMIT_URL", "https://github.com/tyler71/TL-AWS-Analytics/commit")
    sha_msg = f"*[{sha[:6]}]({git_url}/{sha})*"
    return sha_msg
