FROM python:3.10-slim AS build_app

RUN apt-get update \
 && apt-get -y install g++ \
 && rm -r /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim AS build_oauth

RUN apt-get update \
 && apt-get -y install wget \
 && rm -r /var/lib/apt/lists/*

WORKDIR /tmp/download-oauth
RUN wget "https://github.com/oauth2-proxy/oauth2-proxy/releases/download/v7.2.1/oauth2-proxy-v7.2.1.linux-amd64.tar.gz" -O oauth.tar.gz
RUN tar -xf oauth.tar.gz                \
 && mkdir -p /opt/oauth-proxy           \
 && mv oauth2-proxy-*/oauth2-proxy /opt/oauth-proxy/oauth2-proxy \
 && rm oauth.tar.gz


FROM python:3.10-slim AS build_reverse_proxy

RUN apt-get update \
 && apt-get -y install wget \
 && rm -r /var/lib/apt/lists/*

 WORKDIR /tmp/download-reverse-proxy
 RUN wget "https://github.com/caddyserver/caddy/releases/download/v2.4.6/caddy_2.4.6_linux_amd64.tar.gz" -O reverse_proxy.tar.gz
 RUN tar -xf reverse_proxy.tar.gz       \
 && mv caddy /opt/reverse_proxy         \
 && rm reverse_proxy.tar.gz


FROM python:3.10-slim AS production

ENV DATA_DIR /data

COPY --from=build_app           /usr/local         /usr/local
COPY --from=build_oauth         /opt/oauth-proxy   /opt/oauth-proxy
COPY --from=build_reverse_proxy /opt/reverse_proxy /opt/reverse_proxy

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

COPY ./app /app
RUN chown -R application: /app /data

COPY ./config/supervisord.conf /etc/supervisord.conf
COPY ./config/init.sh          /init.sh
COPY ./config/oauth.sh         /opt/oauth-proxy/
COPY ./config/Caddyfile        /etc/Caddyfile

CMD bash /init.sh
