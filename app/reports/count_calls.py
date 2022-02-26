import os
from functools import partial

import duckdb
import pandas as pd
import streamlit as st
from modules import model


def count_calls(df: pd.DataFrame) -> pd.Series:
    tz = os.getenv("TZ", "US/Pacific")
    ts = model.INITTIMESTAMP

    df[ts] = pd.to_datetime(df[ts])
    df[ts] = df[ts].dt.tz_convert(tz)

    download_button_id = st.session_state['widget_id'].__next__()

    col1, col2 = st.columns(2)

    with col1:
        groupby = st.radio("Group by", [
            "Half Hour",
            "Hour",
            "Day",
        ])
        groupby_choice = {
            "Half Hour": partial(group_by, stfr_str='%-I:%M%p', interval='30T'),
            "Hour": partial(group_by, stfr_str='%-I%p'),
            "Day": partial(group_by, stfr_str='%B %d, %Y'),
        }
    query = groupby_choice[groupby](df)

    if not query.empty:
        with col2:
            st.download_button(
                label="Download",
                data=query.to_csv(),
                mime='text/csv',
                key=download_button_id,
            )

    return query


def group_by(df: pd.DataFrame, stfr_str, interval=None) -> pd.Series:
    ts = model.INITTIMESTAMP
    if interval is not None:  # group into specified intervals
        df[ts] = df[ts].dt.floor(interval)
    df[model.DATE_STR] = df[ts].dt.strftime(stfr_str)
    query = """
SELECT {date_str} "Date", COUNT(1) "Count"
 FROM df
 GROUP BY {date_str}
 ORDER BY strptime({date_str},'{stfr_str}')
""".format(date_str=model.DATE_STR, stfr_str=stfr_str)
    query = duckdb.query(query).to_df()

    return query
