import logging
from datetime import date, timedelta

import pandas as pd
import streamlit as st

from modules import model
from pages.fragment.footer import footer

logger = logging.getLogger()

# This fragment is loaded on (all?) pages and provides
# the global settings. Eg, recent metrics versus historical
# it returns a pandas DataFrame

RECENT_METRIC = "Date"
HISTORICAL_METRIC = "Historical"


def boilerplate() -> pd.DataFrame:
    days = 0
    col1, col2 = st.columns(2)

    with col1:
        date_pick = st.date_input(label='Date', min_value=(date.today() - timedelta(days=730)), max_value=date.today())
    with col2:
        clear_cache_button()
        if date_pick != date.today():
            revert_to_today_button()
        historical = st.checkbox('Historical')

    # Ensure slider doesn't get farther than 2 years ago
    if historical:
        t = date.today()
        days_left = (date_pick - (t - timedelta(days=730))).days + 10
        days = st.slider(f'Days from {date_pick}', 0, days_left, value=0, step=10)
    else:
        days = st.slider(f'Days from {date_pick}', 0, 30, value=0, step=1)

    if days < 100:
        loading_text = f"Loading {days} days"
    else:
        loading_text = f"Loading {days} days, there may be a delay"
    with st.spinner(text=loading_text):
        df = model.get_dataframe(days, date_pick)
    if df.empty:
        st.error("No data available!")
        st.stop()

    # df[model.INITTIMESTAMP] = pd.to_datetime(df[model.INITTIMESTAMP])

    footer()

    return df


def add_widget(df, widget):
    if df.empty:
        st.info("Empty")
    else:
        widget(df)

def clear_cache_button():
    button_id = st.session_state['widget_id'].__next__()
    if st.button('Clear Cache', key=button_id):
        st.experimental_memo.clear()
        logger.info("boilerplate, clear cache: Memo cleared")
        st.experimental_singleton.clear()
        logger.info("boilerplate, clear cache: Singleton cleared")

def revert_to_today_button():
    button_id = st.session_state['widget_id'].__next__()
    if st.button('Today', key=button_id):
        date.today()

