import logging
import os
from functools import partial

import duckdb
import pandas as pd
import streamlit as st
from modules import model

from pages.fragment.download_button import download_button
logger = logging.getLogger()


def count_common_array(df: pd.DataFrame, col: str) -> pd.Series:
    radio_id = st.session_state['widget_id'].__next__()

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
            "Annual": partial(group_by_str, date_str='%Y'),
        }
        query = groupby_choice[groupby](df, col)

    with col2:
      download_button(query)

    return query


def group_by_str(df: pd.DataFrame, col: str, date_str: str) -> pd.Series:
    ts = model.INITTIMESTAMP

    df[model.DATE_STR] = df[ts].dt.strftime(date_str)
    df = df.explode(col)
    query = """
SELECT {col}, {date_str}, COUNT(1) count
 FROM df  
 WHERE {col} is not null
 GROUP BY {col}, {date_str}
 ORDER BY {col} ASC, {date_str} ASC, count DESC
""".format(col=col, date_str=model.DATE_STR)
    query = duckdb.query(query).to_df()
    query = query.pivot_table(
        index=col,
        columns=model.DATE_STR,
        values='count',
        fill_value=0,
    )

    return query
