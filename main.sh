#!/usr/bin/env sh

export MPLCONFIGDIR=$HOME/cache/streamlit/mpl
mkdir -p $MPLCONFIGDIR

unset DISPLAY

echo "Starting server.."
streamlit run main.py        \
  --server.headless true
