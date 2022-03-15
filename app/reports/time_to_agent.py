import duckdb
import pandas as pd
import numpy as np
import streamlit as st
from modules import model
import os
from functools import partial

from pages.fragment.custom_button import download_button
from modules.helper import empty_df_msg

@empty_df_msg
def time_to_agent(df: pd.DataFrame) -> pd.Series:
    groupby_id = st.session_state['widget_id'].__next__()
    avg_radio_id = st.session_state['widget_id'].__next__()
    tz = os.getenv("TZ", "US/Pacific")
    ts = model.INITTIMESTAMP
    c_ts = "CONVERTED_TS"

    df[c_ts] = pd.to_datetime(df[ts])
    df[c_ts] = df[c_ts].dt.tz_convert(tz)

    col1, col2, col3 = st.columns(3)

    with col1:
        groupby = st.radio("Group by", [
            "Half Hour",
            "Hour",
            "Day",
        ], key=groupby_id)
    with col2:
        average_radio = st.radio("Average", [
            "Median",
            "Mean",
        ], key=avg_radio_id)
        average_choice = {
          "Median": "median",
          "Mean":   "avg",
        }
        a_c = average_choice[average_radio]

    groupby_choice = {
        "Half Hour": partial(group_by, stfr_str='%-I:%M%p', average=a_c, interval='30T'),
        "Hour": partial(group_by, stfr_str='%-I%p', average=a_c),
        "Day": partial(group_by, stfr_str='%B %d, %Y', average=a_c),
    }
    query = groupby_choice[groupby](df)

    if not query[0].empty:
        with col3:
          download_button(query[0])

    return query


def group_by(df, stfr_str, average=None, interval=None):
    ts = model.INITTIMESTAMP
    c_ts = "CONVERTED_TS"
  
      
    if interval is not None:  # group into specified intervals
        df[c_ts] = df[c_ts].dt.floor(interval)
    df[model.DATE_STR] = df[c_ts].dt.strftime(stfr_str)

    # If no calls ever connected to to agent for this
    # we just set it as NaN
    agt_ts = 'agent_connectedtoagenttimestamp'
    if agt_ts not in df.columns:
        df[agt_ts] = np.nan
        df['time_to_connect'] = np.nan
    else:
        init = pd.to_datetime(df[ts])
        connected = pd.to_datetime(df[agt_ts])
        df['time_to_connect'] = (connected - init).dt.total_seconds()
  
    query = """
SELECT {date_str} "Date", {a}(time_to_connect) "Time to Connect"
 FROM df
  WHERE time_to_connect is not null
 GROUP BY {date_str}
 ORDER BY strptime({date_str}, '{stfr_str}')
""".format(
  date_str=model.DATE_STR, 
  stfr_str=stfr_str,
  a=average,
  ts=model.INITTIMESTAMP,
  agt_ts=agt_ts,
  )
    query = duckdb.query(query).to_df()
  
    return (query, ["Date", "Time to Connect"])