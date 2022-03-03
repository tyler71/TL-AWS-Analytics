import streamlit as st
from pages.fragment.boilerplate import boilerplate
from charts.ctr_list import ctr_list
from reports.menu_wait_list import menu_wait_list


def app():
    # Here we load the global setting widgets (sliders, and such)
    # It returns the dataframe which has the data we need
    df = boilerplate()

    reports = {
      'Wait Time in Menu': (menu_wait_list, ["Menu Wait (M)"])
    }

    options = list(reports.keys())
    options.sort()
  
    selected_report = st.selectbox("Select Report", options)

    output = reports[selected_report][0](df)
    ctr_list(output, reports[selected_report][1])