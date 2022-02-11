import streamlit as st
from functools import partial

from modules import model
from pages.fragment.boilerplate import boilerplate, add_widget

from reports.count_common_array import count_common_array
from reports.count_caller_hangups import count_caller_hangups

def app():

  # Here we load the global settin widgets (sliders, and such)
  # It returns the dataframe which has the data we need
  df = boilerplate()

  # Partials are a good way to pass a _partially_ filled function into
  # another function. Here, we preset the height and width to 600
  # This is similar to st.dataframe(df, height=600, width=600)
  # Since we use add_widget, which has logic for checking the widget
  # This makes everything play nice
  partial_dataframe_widget = partial(st.dataframe, height=600, width=600)

  st.header("Most Common Flows")
  add_widget(count_common_array(df, model.FLOWS), partial_dataframe_widget)

  st.header("Most Common Menu Options")
  add_widget(count_common_array(df, model.MENUS), partial_dataframe_widget)
