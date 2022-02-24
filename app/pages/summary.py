import streamlit as st

from reports.count_common_array import count_common_array
from reports.count_caller_hangups import count_caller_hangups
from reports.count_calls import count_calls
from pages.fragment.boilerplate import boilerplate, add_widget
from charts.bar_chart import bar_chart

# Here we define the expected JSON structure
FLOWS="flowsaccessed"
MENUS="menuoptionselected"



def app():

  df = boilerplate()

  st.header("Count Callers")
  bar_chart(count_calls(df), "Date", "Count")

  # st.header("Most Common Flows")
  # add_widget(count_common_array(df, FLOWS), 
  #            st.bar_chart)

  # st.header("Most Common Menu Options")
  # add_widget(count_common_array(df, MENUS),
  #            st.bar_chart)

  st.header("Caller Hangups by Flow")
  hangups = count_caller_hangups(df)
  add_widget(hangups,
             st.dataframe)
