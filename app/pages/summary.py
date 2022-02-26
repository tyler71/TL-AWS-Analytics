import streamlit as st
from charts.bar_chart import xy_bar_chart
from pages.fragment.boilerplate import boilerplate, add_widget
from reports.count_calls import count_calls


def app():
    df = boilerplate()

    st.header("Count Callers")
    xy_bar_chart(count_calls(df), "Date", "Count")
