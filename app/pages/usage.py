from functools import partial

import streamlit as st
from modules import model
from pages.fragment.boilerplate import boilerplate, add_widget
from reports.flow_caller_hangup import flow_caller_hangup
from reports.count_common_array import count_common_array


def app():
    # Here we load the global setting widgets (sliders, and such)
    # It returns the dataframe which has the data we need
    df = boilerplate()

    # Partials are a good way to pass a _partially_ filled function into
    # another function. Here, we preset the height and width to 600
    # This is similar to st.dataframe(df, height=600, width=600)
    # Since we use add_widget, which has logic for checking the widget
    # This makes everything play nice
    partial_dataframe_widget = partial(st.dataframe, height=600, width=1000)

    st.header("Most Common Flows")
    add_widget(count_common_array(df, model.FLOWS)[0], partial_dataframe_widget)

    st.header("Most Common Menu Options")
    add_widget(count_common_array(df, model.MENUS)[0], partial_dataframe_widget)

    st.header("Caller Hangups by Flow")
    hangups = flow_caller_hangup(df)[0]
    add_widget(hangups, st.dataframe)