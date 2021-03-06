import streamlit as st
from charts.xy_chart import xy_bar_chart,xy_line_chart,xy_area_chart
from pages.fragment.boilerplate import boilerplate
from reports.count_calls import count_calls
from reports.queue_wait import queue_wait
from reports.count_caller_hangup import count_caller_hangup
from reports.time_to_agent import time_to_agent


def app():
    df = boilerplate()

    st.header("Call Count")
    o = count_calls(df)
    if o is not None:
      query, x, y = o[0], o[1][0], o[1][1]
      xy_bar_chart(query, x, y)

    st.header("Time to Agent (Avg)")
    o = time_to_agent(df)
    if o is not None:
      query, x, y = o[0], o[1][0], o[1][1]
      xy_bar_chart(query, x, y)
      

    st.header("Queue Wait Time (Avg)")
    o = queue_wait(df)
    if o is not None:
      query, x, y = o[0], o[1][0], o[1][1]
      xy_area_chart(query, x, y)

    # Hiding hangup count until it's more implemented
    # st.header("Hangup Count")
    # o = count_caller_hangup(df)
    # if o is not None:
    #   query, x, y = o[0], o[1][0], o[1][1]
    #   xy_bar_chart(query, x, y)