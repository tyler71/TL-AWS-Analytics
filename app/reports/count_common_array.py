import pandas as pd
import streamlit as st
import duckdb
import logging
import os

from modules import model

from collections import Counter

logger = logging.getLogger()

# @st.experimental_memo(persist="disk", ttl=600)
def count_common_array(df: pd.DataFrame, col: str) -> pd.Series:
  # """
  # arr = Where in the df the array is
  # ["a", "b", "b", "c"] = ["a": 1, "b": 2, "c": 1]
  # """
  radio_id = st.session_state['widget_id'].__next__()
  download_button_id = st.session_state['widget_id'].__next__()
  
  tz = os.getenv("TIMEZONE", "US/Pacific")
  ts = model.INITTIMESTAMP
  
  df[ts] = pd.to_datetime(df[ts])
  df[ts] = df[ts].dt.tz_convert(tz)

  col1, col2 = st.columns(2)

  with col1:
    groupby = st.radio("Group by", [
      "Month",
      "Annual",
      ],
      key=radio_id)
    groupby_choice = {
      "Month"     : group_by_month,
      "Annual"    : group_by_year,
    }
    query = groupby_choice[groupby](df, col)

  with col2:
    st.download_button(
         label= "Download CSV",
         data = query.to_csv(),
         mime = 'text/csv',
         key  = download_button_id
    )

  return query

def group_by_month(df: pd.DataFrame, col: str) -> pd.Series:
  ts = model.INITTIMESTAMP

  df['date_str'] = df[ts].dt.strftime('%b %Y')
  df = df.explode(col)
  query = """
SELECT {0}, date_str, COUNT(1) count
 FROM df  
 WHERE {0} is not null
 GROUP BY {0}, date_str
 ORDER BY {0} ASC, date_str ASC, count DESC
""".format(col)
  query = duckdb.query(query).to_df()
  query = query.pivot_table(
    index=col, 
    columns='date_str', 
    values='count',
    fill_value=0,
  )

  return query
  
def group_by_year(df: pd.DataFrame, col: str) -> pd.Series:
  ts = model.INITTIMESTAMP
  df['date_str'] = df[ts].dt.strftime('%Y')
  df = df.explode(col)
  query = """
SELECT {0}, date_str, COUNT(1) count
 FROM df  
 WHERE {0} is not null
 GROUP BY {0}, date_str
 ORDER BY {0} ASC, date_str ASC, count DESC
""".format(col)
  query = duckdb.query(query).to_df()
  query = query.pivot_table(
    index=col, 
    columns='date_str', 
    values='count',
    fill_value=0,
  )
  
  return query
