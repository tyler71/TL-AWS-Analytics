import logging
import pandas as pd
import streamlit as st

from modules import model
from modules.helper import minutes_to_hour_minutes

from datetime import date, timedelta
logger = logging.getLogger()

# This fragment is loaded on (all?) pages and provides
# the global settings. Eg, recent metrics versus historical
# it returns a pandas DataFrame

RECENT_METRIC    = "Date"
HISTORICAL_METRIC = "Historical"

def boilerplate() -> pd.DataFrame:

    days = 0
    col1, col2 = st.columns(2)
  
    with col1:
      date_pick = st.date_input(label='Date', min_value=(date.today() - timedelta(days=730)), max_value=date.today())
    with col2:
      if st.button('Clear Cache'):
        st.experimental_memo.clear()
        logger.info("boilerplate, clear cache: Memo cleared")
        st.experimental_singleton.clear()
        logger.info("boilerplate, clear cache: Singleton cleared")

    # Ensure slider doesn't get farther then 2 years ago
    t = date.today()
    days_left = (date_pick - (t - timedelta(days=730))).days + 10
    days = st.slider(f'Days from {date_pick}', 0, days_left, value=0, step=10)

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

    return df

def add_widget(df, widget):
  if df.empty:
    st.info("Empty")
  else:
    widget(df)