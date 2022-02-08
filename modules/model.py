import json
import pandas as pd
import os
import streamlit as st
import concurrent.futures

from modules.helper import get_window_days

mock_data = os.getenv("MOCK_DATA_DIR", False)

# Each file can have multiple JSON objects in it.
# We don't process them here, but pass each individual
# JSON string upwards.
def extract_from_file(data: str) -> str:
  if '}{' in data:
    raw_str = data.replace('}{', '}\0{')
  elif '}\n{' in data:
    raw_str = data.replace('}\n{', '}\0{')
  else:
    raw_str = data
  yield from raw_str.split('\0')

# @st.cache(persist=True, ttl=2_620_800) # 1 month

# Mock data for developing with
if mock_data:
  def get_files(days: int):
      for dir_day in get_window_days(days, prefix=mock_data):
          if(os.path.isdir(dir_day)):
              for f in os.listdir(dir_day):
                  yield os.path.join(dir_day, f)

    # for day in get_window_days(days, prefix='s3/ctr/converted/'):
      # for filenames in os.listdir(day):
      #   print("AHHHHHHH", day)
      #   if filenames:
      #     for filename in filenames:
      #       constructed_filename = os.path.join(day, filename)
      #       yield constructed_filename
  def load_file(filename: str) -> str:
    with open(filename) as f:
      data = f.read()
      yield from extract_from_file(data)

# Loads each file. Splits the load_file request into multiple threads
# each load_file can have a series of json_objects, so we iterate over it
def load_files(days: int):
  with concurrent.futures.ThreadPoolExecutor(8) as exec:
    futures = exec.map(load_file, get_files(days))
    for future in futures:
      yield from future


# @st.experimental_memo(persist="disk", ttl=600)
def get_dataframe(days=30) -> pd.DataFrame:
  # Good for a lot of small files
  df = pd.read_json('\n'.join(list(load_files(days))), lines=True)
  # Good for a lot of large files
  # df = pd.concat(pd.read_json(json_object, lines=True) for json_object in load_files())
  return df
