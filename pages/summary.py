import streamlit as st

from modules.report_functions import count_common_array
from modules.report_functions import count_caller_hangups
from pages.boilerplate import boilerplate

# Here we define the expected JSON structure
FLOWS="flowsaccessed"
MENUS="menuoptionselected"

def app():

  df = boilerplate()

  st.header("Most Common Flows")
  st.bar_chart(count_common_array(df, FLOWS))

  st.header("Most Common Menu Options")
  st.bar_chart(count_common_array(df, MENUS))

  hangups = count_caller_hangups(df)
  hangups = hangups.set_index("Last Flow")
  st.header("Caller Hangups by Flow")
  st.dataframe(hangups)
