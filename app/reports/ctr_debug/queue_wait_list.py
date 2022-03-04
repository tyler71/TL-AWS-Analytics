import duckdb
import pandas as pd
import streamlit as st
from modules import model

from pages.fragment.custom_button import download_button

def queue_wait_list(df: pd.DataFrame) -> pd.Series:
    input_id = st.session_state['widget_id'].__next__()

    min_wait = st.number_input("Mininum Minutes",
                               min_value=1,
                               max_value=99,
                               value=2,
                               step=1,
                               key=input_id,
                              )
  
    query = """
SELECT *, queue_duration "Queue Wait (M)"
 FROM df
  WHERE queue_duration is not null
    AND queue_duration > {queue_wait}
""".format(queue_wait=min_wait)
    query = duckdb.query(query).to_df()

    return query
  
