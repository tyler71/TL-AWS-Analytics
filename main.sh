#!/usr/bin/env sh

export MPLCONFIGDIR=$DATA_DIR/cache/streamlit/mpl
export HOME=/data/
mkdir -p $MPLCONFIGDIR

echo "Starting server.."
streamlit run main.py        \
  --server.port 8501         \
  --server.headless true     \
  --server.address 127.0.0.1
