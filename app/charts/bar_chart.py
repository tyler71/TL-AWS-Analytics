import altair as alt
import pandas as pd
import streamlit as st


def xy_bar_chart(df: pd.DataFrame, ix, iy, sort=None) -> None:
    chart = (alt.Chart(df).mark_bar().encode(
        x=alt.X(ix, sort=sort),
        y=iy,
    ))
    st.altair_chart(chart, use_container_width=True)
