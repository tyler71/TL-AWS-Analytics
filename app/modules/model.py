import logging
import os
import pandas as pd
import streamlit as st
import typing

from modules.helper import get_window_days
from modules.S3Bucket import getS3Bucket

FLOWS         = "flowsaccessed"
MENUS         = "menuoptionselected"
INITTIMESTAMP = "initiationtimestamp"


## Data loading
# The outcome here is to load a dataframe
# To get this, we call load_files, which calls get_files
# get_files operates by directory and calls get_dir
# get_dir returns the strings of all objects found
# by calling extract_from_file. More than one object may
# be in a file
# It is broken up to allow caching at different levels
# Generators cannot be cached.

## Here we either use the S3 implementation or mock
# if bucket_* is set it will use S#
# If mock_data is set, it will use mock
# Mock overrides S3
bucket_name   = os.getenv("BUCKET_NAME", False)
bucket_prefix = os.getenv("BUCKET_PREFIX", False)
mock_data     = os.getenv("MOCK_DATA_DIR", False)

logger = logging.getLogger()

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


if bucket_name and bucket_prefix:
  logging.info(f"S3 Mode is Active")
  def get_files(days: int) -> typing.Generator[str, None, None]:
    for dir_day in get_window_days(days, prefix=bucket_prefix):
      logging.info(f"s3 get_files: Trying day {dir_day}")
      logger.debug(f"s3 get_files: Retrieving files from {dir_day}")
      yield from get_dir(dir_day)
  # We download all the data before returning, should be cached
  # @st.experimental_memo(persist="disk", ttl=600)
  @st.experimental_memo(persist="disk", ttl=900)
  def get_dir(dir_day) -> typing.List[str]:
    logging.info(f"s3 get_dir: loading bucket")
    bucket = getS3Bucket()
    logging.info(f"s3 get_dir: loading objs")
    objs = bucket.objects.filter(Prefix=dir_day)
    logging.info(f"s3 get_dir: {objs}")
    # Here we load the object from S3
    # decode it and put it into a list
    result = [obj.get()['Body'].read().decode() for obj in objs] 
    logging.info(f"s3 get_dir: {dir_day} cached")
    logger.debug(f"s3 get_dir: {result}")
    return result


# Mock data for developing with
# These functions simulate a S3 bucket
if mock_data:
  def get_files(days: int) -> typing.Generator[str, None, None]:
      for dir_day in get_window_days(days, prefix=mock_data):
          logger.debug(f"mock get_files: Retrieving files from {dir_day}")
          yield from get_dir(dir_day)
  @st.experimental_memo(persist="disk", ttl=900)
  def get_dir(dir_day) -> typing.List[str]:
      if os.path.isdir(dir_day):
          filepaths = (os.path.join(dir_day, f) for f in os.listdir(dir_day))

          files = list()
          for filepath in filepaths:
            for obj in load_file(filepath):
              files.append(obj)

          result = files
          logging.info(f"mock get_dir: {dir_day} cached")
          logging.debug(f"mock get_dir: {result}")
          return result
          # return result
      else:
          return list()
  def load_file(filename: str) -> typing.List[str]:
    with open(filename) as f:
      data = f.read()
      logger.debug(f"load_file: {filename} cached")
      return [obj for obj in extract_from_file(data)]

# Loads each file. Splits the load_file request into multiple threads
# each load_file can have a series of json_objects, so we iterate over it
# def load_files(days: int) -> typing.Generator[str, None, None]:
#   yield from get_files(days)
  #   futures = exec.map(load_file, get_files(days))
  #   for future in futures:
  #     yield from future

@st.experimental_memo(persist="disk", ttl=300)
def get_dataframe(days=30) -> pd.DataFrame:
  # We load all the files up to days ago, convert to a list and join with
  # newlines. This is read into a dataframe with pandas
  logger.info(f"get_dataframe: {days} days cached")
  df = pd.read_json('\n'.join(list(get_files(days))), lines=True)
  return df