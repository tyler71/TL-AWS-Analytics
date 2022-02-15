#!/usr/bin/env sh

script_dir="/app"

export MPLCONFIGDIR=$HOME/cache/streamlit/mpl
mkdir -p $MPLCONFIGDIR

# For Replit
unset DISPLAY

# STREAMLIT_SERVER_ADDRESS          = "0.0.0.0"
# STREAMLIT_SERVER_PORT             = "8501"
# STREAMLIT_SERVER_COOKIESECRET     = "cookieSecret2"
# STREAMLIT_BROWSER_SERVERADDRESS   = "https://domain.tld"
# STREAMLIT_CLIENT_SHOWERRORDETAILS = "false"

# If Server Address is not set, but is running under Supervisor,
# set Server Address to 127.0.0.1
if [ -z ${STREAMLIT_SERVER_ADDRESS+x} ] && [ -n ${SUPERVISOR_ENABLED} ]; then
  export STREAMLIT_SERVER_ADDRESS=127.0.0.1
fi

echo "Starting server.."
cd "$script_dir"
streamlit run main.py                       \
  --server.enableCORS                 false \
  --server.enableXsrfProtection       false \
  --server.enableWebsocketCompression false \
  --server.headless                   true
