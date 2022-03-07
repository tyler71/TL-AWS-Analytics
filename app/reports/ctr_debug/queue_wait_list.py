import duckdb
import pandas as pd
import streamlit as st
import numpy as np
from modules import model

from pages.fragment.custom_button import download_button
from modules.helper import time_to_hour_minute_second
from modules.helper import show_empty_dec

@show_empty_dec
def queue_wait_list(df: pd.DataFrame) -> pd.Series:
    input_id = st.session_state['widget_id'].__next__()

    q_dur = model.QUEUE_DUR

    if q_dur not in df:
      df[q_dur] = np.nan

    min_wait = st.number_input("Mininum Seconds",
                               min_value=1, max_value=99,
                               value=30,
                               step=1,
                               key=input_id,
                              )
  
    query = """
SELECT *, {queue_dur} "Queue Wait"
 FROM df
  WHERE {queue_dur} is not null
    AND {queue_dur} > {queue_wait}
""".format(queue_dur=q_dur, queue_wait=min_wait)
    query = duckdb.query(query).to_df()
    query["Queue Wait"] = query["Queue Wait"].apply(lambda x: time_to_hour_minute_second(seconds=x))

    return query
  
