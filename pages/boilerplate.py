import pandas as pd
import streamlit as st

from modules import model
from modules.helper import minutes_to_hour_minutes

def boilerplate():
    metric_type = st.radio('Metric', ["Recent", "Historical"])
    if metric_type == "Historical":
        days = st.slider('How many days ago', 0, 364, value=30, step=10)
    elif metric_type == "Recent":
        minutes = st.slider("How many minutes ago", 0, 480, value=15, step=15)
        if minutes >= 60:
            st.write(minutes_to_hour_minutes(minutes))
        days = 0

    if days < 100:
        loading_text = f"Loading {days} days"
    else:
        loading_text = f"Loading {days} days, there may be a delay"
    with st.spinner(text=loading_text):
        df = model.get_dataframe(days)
    if df.empty:
        st.error("No data available!")
        st.stop()

    if metric_type == "Recent":
        df[model.INITTIMESTAMP] = pd.to_datetime(df[model.INITTIMESTAMP])
        df = df[df[model.INITTIMESTAMP].diff().lt(f'{minutes}Min')]

    return df