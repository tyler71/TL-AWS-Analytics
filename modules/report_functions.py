import pandas as pd
import numpy as np
import duckdb

from collections import Counter

def count_common_array(df: pd.DataFrame, col: str) -> pd.Series:
  """
  arr = Where in the df the array is
  ["a", "b", "b", "c"] = ["a": 1, "b": 2, "c": 1]
  """
  most_common_arrays = df[col].sum()
  most_common_arrays = pd.Series(Counter(most_common_arrays))
  return most_common_arrays

def count_caller_hangups(data: pd.DataFrame) -> pd.Series:
  df = data
  query = """
SELECT attributes_lastflow "Last Flow", 
       COUNT(1) "Count" 
 FROM df
 WHERE DisconnectReason='CUSTOMER_DISCONNECT'
   AND Agent_Username='null'
 GROUP BY attributes_lastflow
"""
  query = duckdb.query(query).to_df()
  list(query)
  # query = pd.Series(query)
  return query