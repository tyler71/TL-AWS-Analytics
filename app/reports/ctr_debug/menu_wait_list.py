import duckdb
import pandas as pd
import numpy as np
import streamlit as st
from modules import model

from modules.helper import time_to_hour_minute_second
from modules.helper import empty_df_msg

@empty_df_msg
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
  
    if model.ENQUEUED_TS not in df:
      df[q_ts] = np.nan
    df[q_ts] = df[q_ts].fillna(0)
    df[q_ts] = (pd.to_datetime(df[q_ts])).astype('int64') / 10 ** 9
    query = """
SELECT *, ({queuets}::int - {initts}::int) "Menu Wait"
 FROM df
  WHERE {queuets} is not null
    AND "Menu Wait" / 60 >= {min_wait}
""".format(queuets=q_ts, initts="conv_ts", min_wait=min_wait)
    query = duckdb.query(query).to_df()
    query["Menu Wait"] = query["Menu Wait"].apply(lambda x: time_to_hour_minute_second(seconds=x))

    return query