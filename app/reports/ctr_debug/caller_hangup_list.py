import os
from functools import partial

import duckdb
import pandas as pd
import streamlit as st
from modules import model
from pages.fragment.custom_button import download_button
from modules.helper import empty_df_msg

@empty_df_msg
def caller_hangup_list(df: pd.DataFrame) -> pd.Series:
    if model.VOICEMAIL not in df.columns:
        df[model.VOICEMAIL] = None
    if model.AGENT not in df.columns:
        df[model.AGENT] = None
    query = """
SELECT *
 FROM df
 WHERE disconnectreason='CUSTOMER_DISCONNECT'
   AND {an} is null
   AND {vm} is null
   AND '*Queue*' NOT LIKE {flows}
""".format(flows=model.FLOWS,
           vm=model.VOICEMAIL,
           an=model.AGENT,
          )
    query = duckdb.query(query).to_df()

    if not df.empty:
          download_button(query)
      
    return query