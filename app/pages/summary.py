import streamlit as st
from charts.xy_chart import xy_bar_chart,xy_line_chart,xy_area_chart
from pages.fragment.boilerplate import boilerplate, add_widget
from reports.count_calls import count_calls
from reports.queue_wait import queue_wait
from reports.count_caller_hangup import count_caller_hangup


def app():
    df = boilerplate()

    st.header("Call Count")
    o = count_calls(df)
    query, x, y = o[0], o[1][0], o[1][1]
    xy_bar_chart(query, x, y)

    st.header("Queue Wait Time (Avg)")
    o = queue_wait(df)
    query, x, y = o[0], o[1][0], o[1][1]
    xy_area_chart(query, x, y)

    st.header("Hangup Count")
    o = count_caller_hangup(df)
    query, x, y = o[0], o[1][0], o[1][1]
    xy_bar_chart(query, x, y)