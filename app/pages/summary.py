import streamlit as st
from charts.xy_chart import xy_bar_chart,xy_line_chart
from pages.fragment.boilerplate import boilerplate, add_widget
from reports.count_calls import count_calls
from reports.queue_wait import queue_wait


def app():
    df = boilerplate()

    st.header("Count Callers")
    xy_bar_chart(count_calls(df), "Date", "Count")

    st.header("Average Queue Wait Time")
    xy_line_chart(queue_wait(df), "Date", "Wait Time")