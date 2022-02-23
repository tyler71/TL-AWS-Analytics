import pandas as pd
import streamlit as st
import duckdb
import os
from modules import model

# @st.experimental_memo(persist="disk", ttl=600)
def count_calls(df: pd.DataFrame) -> pd.Series:
  tz = os.getenv("TIMEZONE", "US/Pacific")
  ts = model.INITTIMESTAMP
  
  df[ts] = pd.to_datetime(df[ts])
  df[ts] = df[ts].dt.tz_convert(tz)

  groupby = st.radio("Group by", [
    "Half Hour",
    "Hour", 
    "Day", 
  ])
  groupby_choice = {
    "Half Hour": group_by_halfhr,
    "Hour"     : group_by_hour,
    "Day"      : group_by_day,
  }
  query = groupby_choice[groupby](df)

  return query

def group_by_hour(df: pd.DataFrame) -> pd.Series:
  ts = model.INITTIMESTAMP
  df['date_str'] = df[ts].dt.strftime('%-I%p')
  query = """
SELECT date_str "Date", COUNT(1) "Count"
 FROM df
 GROUP BY date_str
 ORDER BY strptime(date_str,'%-I%p')
"""
  query = duckdb.query(query).to_df()

  return query

def group_by_day(df: pd.DataFrame) -> pd.Series:
  ts = model.INITTIMESTAMP
  df["date_str"] = df[ts].dt.strftime('%B %d, %Y')
  query = """
SELECT date_str "Date", COUNT(1) "Count"
 FROM df
 GROUP BY date_str
 ORDER BY strptime(date_str, '%B %d, %Y')
"""
  query = duckdb.query(query).to_df()

  return query

def group_by_halfhr(df: pd.DataFrame) -> pd.Series:
  ts = model.INITTIMESTAMP
  # Group into 30 minute intervals
  df[ts] = df[ts].dt.floor('30T')
  df['date_str'] = df[ts].dt.strftime('%-I:%M%p')
  query = """
SELECT date_str "Date", COUNT(1) "Count"
 FROM df
 GROUP BY date_str
 ORDER BY strptime(date_str, '%-I:%M%p')
"""
  query = duckdb.query(query).to_df()

  return query