import duckdb
import pandas as pd
import streamlit as st
from modules import model

from pages.fragment.download_button import download_button

def menu_wait_list(df: pd.DataFrame) -> pd.Series:
    ts = model.INITTIMESTAMP
    q_ts = model.ENQUEUED_TS
    df["conv_ts"] = (pd.to_datetime(df[ts])).astype('int64') / 10 ** 9
    df[q_ts] = df[q_ts].fillna(0)
    df[q_ts] = (pd.to_datetime(df[q_ts])).astype('int64') / 10 ** 9
    query = """
SELECT *, ({queuets}::int - {initts}::int) / 60 "Menu Wait (M)"
 FROM df
  WHERE {queuets} is not null
    AND "Menu Wait (M)" > 1
""".format(queuets=q_ts, initts="conv_ts")
    query = duckdb.query(query).to_df()

    return query