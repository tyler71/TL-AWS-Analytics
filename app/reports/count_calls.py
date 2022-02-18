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

  groupby = st.radio("Group by", ["Day", "Hour", "Half Hour"])
  groupby_choice = {
    "Day"      : group_by_day,
    "Hour"     : group_by_hour,
    "Half Hour": group_by_halfhr,
  }
  query = groupby_choice[groupby](df)

  return query

def group_by_hour(df: pd.DataFrame) -> pd.Series:
  ts = model.INITTIMESTAMP
  df['date_str'] = df[ts].dt.strftime('%-I%p')
  query = """
SELECT date_str "Hour", COUNT(1) "Count"
 FROM df
 GROUP BY date_str
"""
  query = duckdb.query(query).to_df()
  query = query.set_index("Hour")

  return query

def group_by_day(df: pd.DataFrame) -> pd.Series:
  ts = model.INITTIMESTAMP
  # df = (df[ts]
  #       .dt.floor('d')
  #       .dt.strftime('%B %d, %Y')
  #       .value_counts()
  #       .rename_axis('date')
  #       .reset_index(name='Count')
  #       .set_index('date')
  #       )
  df["date_str"] = df[ts].dt.strftime('%B %d, %Y')
  query = """
SELECT date_str "Date", COUNT(1) "Count"
 FROM df
 GROUP BY date_str
"""
  query = duckdb.query(query).to_df()
  query = query.set_index("Date")

  return query

def group_by_halfhr(df: pd.DataFrame) -> pd.Series:
  ts = model.INITTIMESTAMP
  df[ts] = df[ts].dt.floor('30T')
  df['date_str'] = df[ts].dt.strftime('%-I:%M%p')
  query = """
SELECT date_str "Hour", COUNT(1) "Count"
 FROM df
 GROUP BY date_str
"""
  query = duckdb.query(query).to_df()
  query = query.set_index("Hour")

  return query