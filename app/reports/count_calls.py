import os
from functools import partial

import duckdb
import pandas as pd
import numpy as np
import streamlit as st
from modules import model

from pages.fragment.custom_button import download_button

from modules.helper import empty_df_msg

@empty_df_msg
def count_calls(df: pd.DataFrame) -> pd.Series:
    radio_id = st.session_state['widget_id'].__next__()
    agent_id = st.session_state['widget_id'].__next__()
  
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
        ], key=radio_id)
    with col2:
        fa = st.radio("Reached Agent", [
          "All",
          "Agent",
        ], key=agent_id)
      
    groupby_choice = {
        "Half Hour": partial(group_by, stfr_str='%-I:%M%p', agent=fa, interval='30T'),
        "Hour": partial(group_by, stfr_str='%-I%p', agent=fa),
        "Day": partial(group_by, stfr_str='%B %d, %Y', agent=fa),
    }
      
    query = groupby_choice[groupby](df)

    if not query[0].empty:
        with col3:
          download_button(query[0])

    df = df.drop([c_ts], axis=1)
    return query


def group_by(df: pd.DataFrame, stfr_str, interval=None, agent=None) -> pd.Series:
    c_ts = "CONVERTED_TS"
    if interval is not None:  # group into specified intervals
        df[c_ts] = df[c_ts].dt.floor(interval)
    df[model.DATE_STR] = df[c_ts].dt.strftime(stfr_str)

    agt_ts = 'agent_connectedtoagenttimestamp'
    if agt_ts not in df.columns:
        df[agt_ts] = np.nan

    where_str = ''
    if agent == "Agent":
      where_str = f"AND {agt_ts} is not null"
    query = """
SELECT {date_str} "Date", COUNT(1) "Count"
 FROM df
 WHERE initiationmethod='INBOUND'
 {where_str}
 GROUP BY {date_str}
 ORDER BY strptime({date_str},'{stfr_str}')
""".format(date_str=model.DATE_STR, 
           stfr_str=stfr_str,
           where_str=where_str
          )
    query = duckdb.query(query).to_df()

    return (query, ["Date", "Count"])
