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
    footer()
    days = 0
    col1, col2 = st.columns(2)

    with col1:
        date_pick = st.date_input(label='Date', min_value=(date.today() - timedelta(days=730)), max_value=date.today())
    with col2:
        # Ensure slider doesn't get farther than 2 years ago
        if 'historical' in st.session_state and st.session_state['historical'] is True:
            t = date.today()
            days_left = (date_pick - (t - timedelta(days=730))).days + 10
            days = st.slider(days_from_msg(date_pick), 0, days_left, value=0, step=10)
        else:
            days = st.slider(days_from_msg(date_pick), 0, 30, value=0, step=1)
        # clear_cache_button()


    if days < 31:
        loading_text = f"Loading {days} days"
    else:
        loading_text = f"Loading {days} days, there may be a delay"
    with st.spinner(text=loading_text):
        df = model.get_dataframe(days, date_pick)
    if df.empty:
        st.error("No data available!")
        st.stop()

    # df[model.INITTIMESTAMP] = pd.to_datetime(df[model.INITTIMESTAMP])

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

def days_from_msg(date_picked):
    msg = "Days from {date}{today_str}"
    today = date.today()
    formatted_date = date_picked.strftime('%b %d, %Y')
    if date_picked == today:
        msg = msg.format(date=formatted_date, today_str=' (Today)')
    else:
        msg = msg.format(date=formatted_date, today_str='')
    return msg
