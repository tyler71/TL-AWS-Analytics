import pandas as pd
import streamlit as st

def download_button(df):
  if ('show_download' in st.session_state 
    and st.session_state['show_download'] is True):
    id = st.session_state['widget_id'].__next__()
    st.download_button(
        label="Download",
        data=df.to_csv(),
        mime='text/csv',
        key=id,
    )

def rerun_button():
    button_id = st.session_state['widget_id'].__next__()
    if st.button('Refresh', key=button_id):
        st.experimental_rerun()

