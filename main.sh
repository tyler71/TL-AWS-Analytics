#!/usr/bin/env sh

export MPLCONFIGDIR=$DATA_DIR/cache/streamlit/mpl
mkdir -p $MPLCONFIGDIR

echo "Starting server.."
streamlit run main.py        \
  --server.headless true
