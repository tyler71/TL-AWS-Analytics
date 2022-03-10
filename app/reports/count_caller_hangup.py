import os
from functools import partial

import duckdb
import pandas as pd
import streamlit as st
from modules import model
from pages.fragment.custom_button import download_button
from modules.helper import empty_df_msg

@empty_df_msg
def count_caller_hangup(df: pd.DataFrame) -> pd.Series:
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
            "Half Hour": partial(group_by_str, stfr_str='%-I:%M%p', interval='30T'),
            "Hour": partial(group_by_str, stfr_str='%-I%p'),
            "Day": partial(group_by_str, stfr_str='%B %d, %Y'),
        }
    query = groupby_choice[groupby](df)

    if not query[0].empty:
        with col2:
          download_button(query)

    return query

def group_by_str(df, stfr_str, interval=None):
    ts = model.INITTIMESTAMP
    df[model.DATE_STR] = df[ts].dt.strftime(stfr_str)
    if model.VOICEMAIL not in df.columns:
        df[model.VOICEMAIL] = None
    if model.AGENT not in df.columns:
        df[model.AGENT] = None
    query = """
SELECT {date_str} "Date",
       COUNT(1) count
 FROM df
 WHERE disconnectreason='CUSTOMER_DISCONNECT'
   AND {an} is null
   AND {vm} is null
   AND '*Queue*' NOT LIKE {flows}
 GROUP BY {date_str}
 ORDER BY strptime({date_str},'{stfr_str}')
""".format(date_str=model.DATE_STR, 
           stfr_str=stfr_str,
           flows=model.FLOWS,
           vm=model.VOICEMAIL,
           an=model.AGENT,
          )
    query = duckdb.query(query).to_df()
    return (query, ["Date", "count"])
