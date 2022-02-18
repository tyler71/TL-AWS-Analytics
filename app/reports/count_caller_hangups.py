import pandas as pd
import streamlit as st
import duckdb

@st.experimental_memo(persist="disk", ttl=600)
def count_caller_hangups(df: pd.DataFrame) -> pd.Series:
  query = """
SELECT attributes_lastflow "Last Flow", 
       COUNT(1) "Count" 
 FROM df
 WHERE DisconnectReason='CUSTOMER_DISCONNECT'
   AND Agent_Username='null'
 GROUP BY attributes_lastflow
"""
  query = duckdb.query(query).to_df()
  # list(query)
  # query = pd.Series(query)
  return query