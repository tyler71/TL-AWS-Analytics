#!/usr/bin/env sh

export MPLCONFIGDIR=$HOME/cache/streamlit/mpl
mkdir -p $MPLCONFIGDIR

# For Replit
unset DISPLAY

# STREAMLIT_SERVER_ADDRESS          = "0.0.0.0"
# STREAMLIT_SERVER_PORT             = "8501"
# STREAMLIT_SERVER_COOKIESECRET     = "cookieSecret2"
# STREAMLIT_BROWSER_SERVERADDRESS   = "https://domain.tld"
# STREAMLIT_CLIENT_SHOWERRORDETAILS = "false"

echo "Starting server.."
streamlit run main.py        \
  --server.headless true
