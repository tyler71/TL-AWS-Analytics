import streamlit as st
import pandas as pd

import modules.model

from modules.report_functions import count_common_array
from modules.report_functions import count_caller_hangups

FLOWS="flowsaccessed"
MENUS="menuoptionselected"

def app():

  metric_type = st.radio('Metric', ["Recent", "Historical"])
  if metric_type == "Historical":
    days = st.slider('How many days ago', 0, 364, value=30, step=10)
  elif metric_type == "Recent":
    minutes = st.slider('How many minutes ago', 0, 480, value=15, step=15)
    days = 0

  df = modules.model.get_dataframe(days)
  if df.empty:
    st.error("No data available!")
    st.stop()

  if metric_type == "Recent":
    df['initiationtimestamp'] = pd.to_datetime(df['initiationtimestamp'])
    df = df[df['initiationtimestamp'].diff().lt(f'{minutes}Min')]

  if df.empty:
    st.error("No data available!")
    st.stop()

  st.header("Most Common Flows")
  
  st.bar_chart(count_common_array(df, FLOWS))

  st.header("Most Common Menu Options")
  st.bar_chart(count_common_array(df, MENUS))

  changups = count_caller_hangups(df)
  changups = changups.set_index("Last Flow")
  st.header("Caller Hangups by Flow")
  st.dataframe(changups)
