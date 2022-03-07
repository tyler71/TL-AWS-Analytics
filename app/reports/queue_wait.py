import duckdb
import pandas as pd
import streamlit as st
from modules import model
from pprint import pprint
import os
from functools import partial

from pages.fragment.custom_button import download_button

from modules import model

from modules.helper import empty_df_msg
@empty_df_msg
def queue_wait(df: pd.DataFrame) -> pd.Series:
    radio_id = st.session_state['widget_id'].__next__()
    tz = os.getenv("TZ", "US/Pacific")
    ts = model.INITTIMESTAMP

    df[ts] = pd.to_datetime(df[ts])
    df[ts] = df[ts].dt.tz_convert(tz)

    col1, col2 = st.columns(2)

    with col1:
        groupby = st.radio("Group by", [
            "Half Hour",
            "Hour",
            "Day",
        ], key=radio_id)
        groupby_choice = {
            "Half Hour": partial(group_by, stfr_str='%-I:%M%p', interval='30T'),
            "Hour": partial(group_by, stfr_str='%-I%p'),
            "Day": partial(group_by, stfr_str='%B %d, %Y'),
        }
    query = groupby_choice[groupby](df)

    if not query.empty:
        with col2:
          download_button(query)

    return query


def group_by(df, stfr_str, interval=None):
    if 'queue_duration' not in df.columns:
        df['queue_duration'] = None
    ts = model.INITTIMESTAMP
    if interval is not None:  # group into specified intervals
        df[ts] = df[ts].dt.floor(interval)
    df[model.DATE_STR] = df[ts].dt.strftime(stfr_str)
    query = """
SELECT {date_str} "Date", median(queue_duration) "Wait Time"
 FROM df
  WHERE queue_duration is not null
    AND queue_duration > 1.0
 GROUP BY {date_str}
 ORDER BY strptime({date_str},'{stfr_str}')
""".format(date_str=model.DATE_STR, stfr_str=stfr_str)
    query = duckdb.query(query).to_df()
    return query