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


FROM caddy:builder AS build_reverse_proxy
ENV XCADDY_SKIP_CLEANUP=1

RUN xcaddy build v2.4.6

RUN mkdir -p /opt/reverse_proxy  \
&& mv /usr/bin/caddy /opt/reverse_proxy/caddy


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

COPY ./config/init/supervisord.conf   /etc/supervisord.conf
COPY ./config/init.sh                 /init.sh
COPY ./config/oauth/oauth.sh          /opt/oauth-proxy/
COPY ./config/reverse_proxy/Caddyfile /etc/Caddyfile

EXPOSE 8080
EXPOSE 4443

CMD bash /init.sh
