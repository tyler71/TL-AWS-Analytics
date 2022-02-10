import logging
import os
import pandas as pd
import streamlit as st
import typing

from modules.helper import get_window_days

FLOWS         = "flowsaccessed"
MENUS         = "menuoptionselected"
INITTIMESTAMP = "initiationtimestamp"

logger = logging.getLogger(__name__)

# Each file can have multiple JSON objects in it.
# We split up the JSON objects and yield them
# one at a time
def extract_from_file(data: str) -> str:
  logger.debug(f"extract_from_file:\n{data}")
  if '}{' in data:
    raw_str = data.replace('}{', '}\0{')
  elif '}\n{' in data:
    raw_str = data.replace('}\n{', '}\0{')
  else:
    raw_str = data
  yield from raw_str.split('\0')


# Do we have mock data to work with?
# If so, use that directory
mock_data = os.getenv("MOCK_DATA_DIR", False)

# Mock data for developing with
# These functions simulate a S3 bucket
if mock_data:
  def get_files(days: int):
      for dir_day in get_window_days(days, prefix=mock_data):
          logger.info(f"get_files: Retrieving files from {dir_day}")
          yield from get_dir(dir_day)
  # @st.experimental_memo(persist="disk", ttl=600)
  def get_dir(dir_day):
      if os.path.isdir(dir_day):
          return [os.path.join(dir_day, f) for f in os.listdir(dir_day)]
      else:
          return tuple()



# Loads each file. Splits the load_file request into multiple threads
# each load_file can have a series of json_objects, so we iterate over it
def load_files(days: int) -> typing.Generator[str, None, None]:
  for day in get_files(days):
    yield from load_file(day)
  #   futures = exec.map(load_file, get_files(days))
  #   for future in futures:
  #     yield from future

# This takes a given local file and returns a tuple
# of JSON objects
@st.experimental_memo(persist="disk", ttl=600)
def load_file(filename: str) -> typing.List[str]:
  with open(filename) as f:
    data = f.read()
    logger.info(f"load_file: loading {filename}")
    return [obj for obj in extract_from_file(data)]


#@st.experimental_memo(persist="disk", ttl=600)
def get_dataframe(days=30) -> pd.DataFrame:
  # We load all the files up to days ago, convert to a list and join with
  # newlines. This is read into a dataframe with pandas
  df = pd.read_json('\n'.join(list(load_files(days))), lines=True)
  return df