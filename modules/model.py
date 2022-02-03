import json
import glob
import pandas as pd
import streamlit as st

@st.cache(persist=True, ttl=2_620_800) # 1 month
def get_file(filename: str) -> list:
  with open(filename) as f:
    data = f.read()
    if '}{' in data:
      raw_str = data.replace('}{', '}\0{')
    elif '}\n{' in data:
      raw_str = data.replace('}\n{', '}\0{')
    else:
      raw_str = data
    json_objects = [json.loads(x) for x in raw_str.split('\0')]
  return json_objects

# @st.cache(persist=True, ttl=600)
def get_files():
  json_files = glob.glob("mock_s3/*", recursive=False)
  json_data = list()
  for fo in json_files:
    json_data += get_file(fo)
  return json_data

def get_dataframe():
  df = pd.read_json(json.dumps(get_files()))
  return df