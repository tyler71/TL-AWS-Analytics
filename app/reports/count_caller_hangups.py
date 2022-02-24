import duckdb
import os
import pandas as pd
import streamlit as st
from modules import model

def count_caller_hangups(df: pd.DataFrame) -> pd.Series:
    col = 'attributes_lastflow'

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
  
    if not query.empty:
      with col2:
          st.download_button(
               label= "Download CSV",
               data = query.to_csv(),
               mime = 'text/csv',
               key  = download_button_id,
          )
  
    return query

def group_by_month(df, col: str):
  ts = model.INITTIMESTAMP
  df['date_str'] = df[ts].dt.strftime('%b %Y')
  print(df)
  query = """
SELECT {0} "Last Flow", 
       date_str, 
       COUNT(1) count
 FROM df  
 WHERE disconnectreason='CUSTOMER_DISCONNECT'
 GROUP BY {0}, date_str
 ORDER BY {0} ASC, date_str ASC, count DESC
""".format(col)
 # WHERE DisconnectReason='CUSTOMER_DISCONNECT'
 #   AND Agent_Username='null'
  query = duckdb.query(query).to_df()
  query = query.pivot_table(
    index="Last Flow", 
    columns='date_str', 
    values='count',
    fill_value=0,
  )
  return query
  
def group_by_year(df, col: str):
  ts = model.INITTIMESTAMP
  df['date_str'] = df[ts].dt.strftime('%Y')
  query = """
SELECT {0} "Last Flow", 
       date_str, 
       COUNT(1) count
 FROM df  
 WHERE DisconnectReason='CUSTOMER_DISCONNECT'
   AND Agent_Username is null
 GROUP BY {0}, date_str
 ORDER BY {0} ASC, date_str ASC, count DESC
""".format(col)
  query = duckdb.query(query).to_df()
  query = query.pivot_table(
    index="Last Flow", 
    columns='date_str', 
    values='count',
    fill_value=0,
  )
  return query