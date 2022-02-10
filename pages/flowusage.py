import streamlit as st

from modules import model
from modules.report_functions import count_common_array, count_caller_hangups
from pages.boilerplate import boilerplate

def app():

  df = boilerplate()

  st.header("Most Common Flows")
  st.dataframe(count_common_array(df, model.FLOWS), height=600, width=600)

  st.header("Most Common Menu Options")
  st.dataframe(count_common_array(df, model.MENUS), height=600, width=600)