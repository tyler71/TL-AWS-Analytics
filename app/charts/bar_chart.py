import altair as alt
import streamlit as st
import pandas as pd


def bar_chart(df: pd.DataFrame, ix, iy, sort=None) -> None:
  if df.empty:
    st.info("Empty")
  else:
    chart = (alt.Chart(df).mark_bar().encode(
        x=alt.X(ix, sort=sort),
        y=iy,
    ))
    st.altair_chart(chart, use_container_width=True)