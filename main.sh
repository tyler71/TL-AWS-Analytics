#!/usr/bin/env bash

current_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export MPLCONFIGDIR=$current_dir/cache/mpl
mkdir -p $MPLCONFIGDIR

echo "Starting server.."
streamlit run main.py       \
  --server.port 8000        \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.headless true    \
  --server.address 127.0.0.1
