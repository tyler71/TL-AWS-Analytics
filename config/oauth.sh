#!/usr/bin/env bash

## Required environment variables
# OAUTH2_PROXY_PROVIDER
# OAUTH2_PROXY_CLIENT_ID
# OAUTH2_PROXY_CLIENT_SECRET
# OAUTH2_PROXY_OIDC_ISSUER_URL
# OAUTH2_PROXY_EMAIL_DOMAIN
# OAUTH2_PROXY_COOKIE_SECRET
# OAUTH2_PROXY_REVERSE_PROXY


/opt/oauth-proxy/oauth2-proxy           \
   --upstream="http://127.0.0.1:8501/"  \
   --http-address="http://0.0.0.0:4180"

