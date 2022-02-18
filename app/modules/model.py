import logging
import os
import pandas as pd
import streamlit as st
import typing

from modules.helper import get_window_days
from modules.s3bucket import get_s3_bucket

FLOWS         = "flowsaccessed"
MENUS         = "menuoptionselected"
INITTIMESTAMP = "initiationtimestamp"
INIT30MIN     = "InitTimeStamp30MinSegment"


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
# Example BUCKET_PREFIX = dir/2022/01/02
bucket_name   = os.getenv("BUCKET_NAME", False)
bucket_prefix = os.getenv("BUCKET_PREFIX", False)
mock_data     = os.getenv("MOCK_DATA_DIR", False)

logger = logging.getLogger()

# Each file can have multiple JSON objects in it.
# We split up the JSON objects and yield them
# one at a time
def extract_from_file(data: str) -> typing.Generator[str, None, None]:
  logger.debug(f"extract_from_file:\n{data}")
  if '}{' in data:
    raw_str = data.replace('}{', '}\0{')
  elif '}\n{' in data:
    raw_str = data.replace('}\n{', '}\0{')
  else:
    raw_str = data
  yield from raw_str.split('\0')


# Loading from S3
if bucket_name and bucket_prefix:
  logging.debug(f"using S3")
  def get_files(days: int) -> typing.Generator[str, None, None]:
    for dir_day in get_window_days(days, prefix=bucket_prefix):
      logger.debug(f"s3 get_files: Retrieving files from {dir_day}")
      yield from get_dir(dir_day)

  @st.experimental_memo(persist="disk", ttl=900)
  def get_dir(dir_day) -> typing.List[str]:
    logging.debug(f"S3 get_dir: loading bucket")
    bucket = get_s3_bucket()
    logging.debug(f"S3 get_dir: bucket {bucket}")

    logging.debug(f"S3 get_dir: loading objs, prefix: {dir_day}")
    objs = bucket.objects.filter(Prefix=dir_day)
    logging.debug(f"S3 get_dir: loaded objs {objs}")

    # Here we load the object from S3
    # decode it and put it into a list

    result = list()
    for obj in objs:
      for data in load_file(obj):
        result.append(data)
  
    logger.debug(f"S3 get_dir: {result}")
    logging.info(f"S3 get_dir: {dir_day} cached")
    return result

  @st.experimental_memo(persist="disk", ttl=2_628_000)
  def load_file(obj: str) -> typing.List[str]:
    logger.debug(f"load_file: {obj} cached")

    data = obj.get()['Body'].read().decode()
    return [obj for obj in extract_from_file(data)]


# Mock data for developing with
# These functions simulate a S3 bucket
if mock_data:
  logging.debug(f"using Mock")
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
          logging.debug(f"mock get_dir: {dir_day} is not a directory")
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
  if (bucket_name and bucket_prefix) or mock_data:
    logger.info(f"get_dataframe: {days} days cached")
    df = pd.read_json('\n'.join(list(get_files(days))), lines=True)
    return df
  else:
    raise Exception("BUCKET_NAME and BUCKET_PREFIX or MOCK_DATA_DIR must be provided!")

  # We load all the files up to days ago, convert to a list and join with
  # newlines. This is read into a dataframe with pandas
