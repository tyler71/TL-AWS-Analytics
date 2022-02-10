import streamlit as st

from modules.report_functions import count_common_array
from modules.report_functions import count_caller_hangups
from pages.fragment.boilerplate import boilerplate, add_widget

# Here we define the expected JSON structure
FLOWS="flowsaccessed"
MENUS="menuoptionselected"



def app():

  df = boilerplate()

  st.header("Most Common Flows")
  add_widget(count_common_array(df, FLOWS), 
             st.bar_chart)

  st.header("Most Common Menu Options")
  add_widget(count_common_array(df, MENUS),
             st.bar_chart)

  st.header("Caller Hangups by Flow")
  hangups = count_caller_hangups(df)
  hangups = hangups.set_index("Last Flow")
  add_widget(hangups,
             st.dataframe)
