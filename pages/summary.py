import streamlit as st
import pandas as pd

import modules.model

from modules.report_functions import count_common_array
from modules.report_functions import count_caller_hangups

FLOWS="flowsaccessed"
MENUS="menuoptionselected"

def app():
  df = modules.model.get_dataframe()

  st.header("Input")
  st.date_input('Your birthday')

  st.header("Most Common Flows")
  st.bar_chart(count_common_array(df, FLOWS))

  st.header("Most Common Menu Options")
  st.bar_chart(count_common_array(df, MENUS))

  changups = count_caller_hangups(df)
  changups = changups.set_index("Last Flow")
  st.header("Caller Hangups by Flow")
  st.dataframe(changups)
