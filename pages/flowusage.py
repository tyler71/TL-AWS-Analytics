import streamlit as st
import pandas as pd

import modules.model

from modules.report_functions import count_common_array, count_caller_hangups

FLOWS="flowsaccessed"
MENUS="menuoptionselected"

def app():
  df = modules.model.get_dataframe()
  if df.empty:
    st.error("No data available!")
    st.stop()

  st.header("Most Common Flows")
  st.dataframe(count_common_array(df, FLOWS), height=600, width=600)

  st.header("Most Common Menu Options")
  st.dataframe(count_common_array(df, MENUS), height=600, width=600)