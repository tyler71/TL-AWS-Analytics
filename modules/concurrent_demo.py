import concurrent.futures
import os
import time

def get_files(dir):
  for dirpath, dirnames, filenames in os.walk(dir):
    if filenames:
      yield from filenames
def get_files(dir):
    for j in range(250):
        #time.sleep(0.2)
        for i in range(30):
            yield f"{j}/{i}"
        
def process_file(filename):
    time.sleep(0.1)
    #print(f"\tprocessing {filename}")
    return f"{filename} done"

with concurrent.futures.ThreadPoolExecutor(3) as exec:
    futures = exec.map(process_file, get_files("files"))
    
    for result in futures:
        print(result)
