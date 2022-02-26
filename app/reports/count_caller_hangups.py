import os
from functools import partial

import duckdb
import pandas as pd
import streamlit as st
from modules import model


def count_caller_hangups(df: pd.DataFrame) -> pd.Series:
    radio_id = st.session_state['widget_id'].__next__()
    download_button_id = st.session_state['widget_id'].__next__()

    tz = os.getenv("TZ", "US/Pacific")
    ts = model.INITTIMESTAMP

    df[ts] = pd.to_datetime(df[ts])
    df[ts] = df[ts].dt.tz_convert(tz)

    col1, col2 = st.columns(2)

    with col1:
        groupby = st.radio("Group by", ["Month", "Annual"],
                           key=radio_id)
        groupby_choice = {
            "Month": partial(group_by_str, date_str='%b %Y'),
            "Annual": partial(group_by_str, date_str="%Y"),
        }
        query = groupby_choice[groupby](df, model.LAST_FLOW)

    if not query.empty:
        with col2:
            st.download_button(
                label="Download",
                data=query.to_csv(),
                mime='text/csv',
                key=download_button_id,
            )

    return query


def group_by_str(df, col: str, date_str: str):
    ts = model.INITTIMESTAMP
    df[model.DATE_STR] = df[ts].dt.strftime(date_str)
    query = """
SELECT {col} "Last Flow",
       {date_str},
       COUNT(1) count
 FROM df
 WHERE disconnectreason='CUSTOMER_DISCONNECT'
   AND Agent_Username is null
 GROUP BY {col}, {date_str}
 ORDER BY {col} ASC, {date_str} ASC, count DESC
""".format(col=col, date_str=model.DATE_STR)
    query = duckdb.query(query).to_df()
    query = query.pivot_table(
        index="Last Flow",
        columns=model.DATE_STR,
        values='count',
        fill_value=0,
    )
    return query
