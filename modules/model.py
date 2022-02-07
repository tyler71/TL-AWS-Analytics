import json
import pandas as pd
import os
import concurrent.futures

mock_data = os.getenv("MOCK_DATA_DIR", False)

# @st.cache(persist=True, ttl=2_620_800) # 1 month
def load_file(filename: str) -> str:
  with open(filename) as f:
    data = f.read()
    if '}{' in data:
      raw_str = data.replace('}{', '}\0{')
    elif '}\n{' in data:
      raw_str = data.replace('}\n{', '}\0{')
    else:
      raw_str = data
    json_objects = (json.loads(x) for x in raw_str.split('\0'))
    yield from json_objects

if mock_data:
  def get_files():
    for dirpath, dirnames, filenames in os.walk(mock_data):
      if filenames:
        for filename in filenames:
          constructed_filename = os.path.join(dirpath, filename)
          yield constructed_filename

def load_files():
  with concurrent.futures.ThreadPoolExecutor(8) as exec:
    futures = exec.map(load_file, get_files())
    for future in futures:
      yield from future


# @st.experimental_memo(persist="disk", ttl=600)
def get_dataframe():
  df = pd.read_json(json.dumps(list(load_files())))
  return df
