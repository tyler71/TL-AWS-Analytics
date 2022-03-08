import streamlit as st
from charts.xy_chart import xy_bar_chart,xy_line_chart,xy_area_chart
from pages.fragment.boilerplate import boilerplate, add_widget
from reports.count_calls import count_calls
from reports.queue_wait import queue_wait
from reports.count_caller_hangup import count_caller_hangup


def app():
    df = boilerplate()

    st.header("Call Count")
    xy_bar_chart(count_calls(df), "Date", "Count")

    st.header("Queue Wait Time (Avg)")
    xy_area_chart(queue_wait(df), "Date", "Wait Time")

    st.header("Hangup Count")
    xy_bar_chart(count_caller_hangup(df), "Date", "count")