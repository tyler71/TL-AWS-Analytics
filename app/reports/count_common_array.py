import pandas as pd
import streamlit as st
import duckdb
import logging

from collections import Counter

logger = logging.getLogger()

# @st.experimental_memo(persist="disk", ttl=600)
def count_common_array(df: pd.DataFrame, col: str) -> pd.Series:
  # """
  # arr = Where in the df the array is
  # ["a", "b", "b", "c"] = ["a": 1, "b": 2, "c": 1]
  # """
  most_common_arrays = df[col].sum()
  most_common_arrays = pd.Series(Counter(most_common_arrays))
  return most_common_arrays
