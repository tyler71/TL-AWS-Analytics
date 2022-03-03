import streamlit as st
from pages.fragment.download_button import download_button
from modules import model
import os
import pandas as pd


def ctr_list(df: pd.DataFrame, columns=list()) -> None:
    # Takes dataframe, shows contact id as a link and sorted Desc by date
    # Then lists any columns provided to it
    # Shown as markdown table
    # CTR_RECORD_URL: The link to a CTR in Amazon Connect, eg
    # https://domain.tld/contact-trace-records/details

    if df.empty:
      st.info("Empty")
      st.stop()
    ctr_url = os.getenv("CTR_RECORD_URL", False)
    if not ctr_url:
        st.error("CTR_RECORD_URL must be set")
        st.stop()
      
    ctr_addr = '[{id}]({ctr_url}/{id})'

    tz = os.getenv("TZ", "US/Pacific")
    ts = model.INITTIMESTAMP

    df[ts] = pd.to_datetime(df[ts])
    df[ts] = df[ts].dt.tz_convert(tz)
  
    df[model.DATE_STR] = df[ts].dt.strftime('%b %d, %Y %I:%M%p')
    df = df.sort_values(by=[ts], ascending=False)

    df = df[["contactid", model.DATE_STR] + columns]
    df['contactid'] = df['contactid'].apply(lambda x: ctr_addr.format(id=x, ctr_url=ctr_url))

    download_button(df)

    st.markdown(df.to_markdown(index=False))