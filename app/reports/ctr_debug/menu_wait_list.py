import duckdb
import pandas as pd
import streamlit as st
from modules import model

from pages.fragment.custom_button import download_button

def menu_wait_list(df: pd.DataFrame) -> pd.Series:
    input_id = st.session_state['widget_id'].__next__()

    min_wait = st.number_input("Mininum Minutes",
                               min_value=1,
                               max_value=99,
                               value=2,
                               step=1,
                               key=input_id,
                              )
  
    ts = model.INITTIMESTAMP
    q_ts = model.ENQUEUED_TS
    df["conv_ts"] = (pd.to_datetime(df[ts])).astype('int64') / 10 ** 9
    df[q_ts] = df[q_ts].fillna(0)
    df[q_ts] = (pd.to_datetime(df[q_ts])).astype('int64') / 10 ** 9
    query = """
SELECT *, ({queuets}::int - {initts}::int) / 60 "Menu Wait (M)"
 FROM df
  WHERE {queuets} is not null
    AND "Menu Wait (M)" >= {min_wait}
""".format(queuets=q_ts, initts="conv_ts", min_wait=min_wait)
    query = duckdb.query(query).to_df()

    return query