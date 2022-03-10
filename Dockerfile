# This stage installs all the requirements for the main app.
# This will be copied later to the production stage
FROM python:3.8-slim AS build_app_environment

RUN apt-get update \
 && apt-get -y install g++ \
 && rm -r /var/lib/apt/lists/*

COPY ./requirements.txt .
#RUN python -m pip install --no-deps --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt


# oauth is handled by oauth2-proxy. This is a Go app, so we just need to
# download the app and put it in a predictible place for the production stage
FROM python:3.8-slim AS build_oauth
ENV OAUTH_DOWNLOAD="https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.2.1/oauth2-proxy-v7.2.1.linux-amd64.tar.gz"

RUN apt-get update \
 && apt-get -y install wget \
 && rm -r /var/lib/apt/lists/*

WORKDIR /tmp/download-oauth
RUN wget "$OAUTH_DOWNLOAD" -O oauth.tar.gz
RUN tar -xf oauth.tar.gz                \
 && mkdir -p /opt/oauth-proxy           \
 && mv oauth2-proxy-*/oauth2-proxy /opt/oauth-proxy/oauth2-proxy \
 && rm oauth.tar.gz


# caddy handles http/s termination. It is built from scratch
# This allows for additional modules later if we need it.
FROM caddy:builder AS build_reverse_proxy
ENV XCADDY_SKIP_CLEANUP=1
ENV BUILD_VERSION=v2.4.6

RUN xcaddy build $BUILD_VERSION

RUN mkdir -p /opt/reverse_proxy  \
&& mv /usr/bin/caddy /opt/reverse_proxy/caddy


# Copy files from previous stages
# We also copy in config files
# A application user is created. While the image doesn't force non-root
# Supervisor later on drops root for all apps it handles
FROM python:3.8-slim AS production

ARG SET_GIT_SHA=dev
ENV GIT_SHA=$SET_GIT_SHA

ENV DATA_DIR /data

COPY --from=build_app_environment /usr/local         /usr/local
COPY --from=build_oauth           /opt/oauth-proxy   /opt/oauth-proxy
COPY --from=build_reverse_proxy   /opt/reverse_proxy /opt/reverse_proxy

RUN mkdir /app /data               \
 && groupadd application           \
      --gid 1000                   \
 && useradd application            \
      --base-dir /app              \
      --home-dir /home/application \
      --create-home                \
      --uid 1000                   \
      --gid 1000                   \
      --system

COPY ./config/init/supervisord.conf   /etc/supervisord.conf
COPY ./config/init.sh                 /init.sh
COPY ./config/oauth/oauth.sh          /opt/oauth-proxy/
COPY ./config/reverse_proxy/Caddyfile /etc/Caddyfile

EXPOSE 8080
EXPOSE 4443

COPY ./app /app
RUN chown -R application: /app /data

CMD bash /init.sh
