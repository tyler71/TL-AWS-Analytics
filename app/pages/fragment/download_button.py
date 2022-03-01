import pandas as pd
import streamlit as st

def download_button(df):
  id = st.session_state['widget_id'].__next__()
  st.download_button(
      label="Download",
      data=df.to_csv(),
      mime='text/csv',
      key=id,
  )