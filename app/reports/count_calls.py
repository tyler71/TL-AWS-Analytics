import os
from functools import partial

import duckdb
import pandas as pd
import streamlit as st
from modules import model

from pages.fragment.custom_button import download_button

from modules.helper import empty_df_msg

@empty_df_msg
def count_calls(df: pd.DataFrame) -> pd.Series:
    groupby_id = st.session_state['widget_id'].__next__()
    avgtype_id = st.session_state['widget_id'].__next__()
    tz = os.getenv("TZ", "US/Pacific")
    ts = model.INITTIMESTAMP

    df[ts] = pd.to_datetime(df[ts])
    df[ts] = df[ts].dt.tz_convert(tz)

    col1, col2, col3 = st.columns(3)

    with col1:
        groupby = st.radio("Group by", [
            "Half Hour",
            "Hour",
            "Day",
        ], key=groupby_id)
    with col2:
        average_type = st.radio("Average", [
            "Median",
            "Mean",
            "Count",
        ], key=avgtype_id)
      
    groupby_choice = {
        "Half Hour": partial(group_by, stfr_str='%-I:%M%p', interval='30T', avg_t=average_type),
        "Hour": partial(group_by, stfr_str='%-I%p', avg_t=average_type),
        "Day": partial(group_by, stfr_str='%B %d, %Y', avg_t=average_type),
    }
    query = groupby_choice[groupby](df)

    if not query.empty:
        with col3:
          download_button(query)

    return query


def group_by(df: pd.DataFrame, stfr_str, interval=None, avg_t=None) -> pd.Series:
    ts = model.INITTIMESTAMP
    if interval is not None:  # group into specified intervals
        df[ts] = df[ts].dt.floor(interval)
    if avg_t == 'Count':
        df[model.DATE_STR] = df[ts].dt.strftime(stfr_str)
        query = """
    SELECT {date_str} "Date", COUNT(1) "Count"
     FROM df
     GROUP BY {date_str}
     ORDER BY strptime({date_str},'{stfr_str}')
    """.format(date_str=model.DATE_STR, stfr_str=stfr_str)
        query = duckdb.query(query).to_df()
    elif avg_t == 'Median':
        df[model.DATE_STR] = df[ts].dt.strftime(stfr_str + '%d')
        query = """
    SELECT {date_str1} "Date" median("Date") 
     FROM (SELECT {date_str} "Date" FROM df)
    """.format(date_str=model.DATE_STR, 
               date_str1=stfr_str,
               stfr_str1=stfr_str + '%d',
              )
        query = duckdb.query(query).to_df()

    return query
