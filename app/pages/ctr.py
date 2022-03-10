import streamlit as st
from pages.fragment.boilerplate import boilerplate
from charts.ctr_list import ctr_list
from reports.ctr_debug.menu_wait_list import menu_wait_list
from reports.ctr_debug.queue_wait_list import queue_wait_list
from reports.ctr_debug.caller_hangup_list import caller_hangup_list
from reports.ctr_debug.custom_list import custom_list


def app():
    # Here we load the global setting widgets (sliders, and such)
    # It returns the dataframe which has the data we need
    df = boilerplate()

    reports = {
      'Wait Time in Menu': (menu_wait_list, ["Menu Wait"]),
      'Wait Time in Queue': (queue_wait_list, ["Queue Wait"]),
      'Custom List': (custom_list, list()),
      'Caller Hangups': (caller_hangup_list, list()),
    }

    options = list(reports.keys())
    options.sort()
  
    selected_report = st.selectbox("Select Report", options)

    output = reports[selected_report][0](df)
    ctr_list(output, reports[selected_report][1])