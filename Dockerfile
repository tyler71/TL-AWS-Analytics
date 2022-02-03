FROM python:3.10-slim AS build

RUN apt-get update \
 && apt-get -y install g++ \
 && rm -r /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim

COPY --from=build /usr/local /usr/local

RUN mkdir /app                     \
 && groupadd application           \
      --gid 1000                   \
 && useradd application            \
      --base-dir /app              \
      --home-dir /home/application \
      --create-home                \
      --uid 1000                   \
      --gid 1000                   \
      --system

COPY . /app
RUN chown -R application: /app

COPY ./config/supervisord.conf /etc/supervisord.conf
COPY ./config/init.sh /init.sh

CMD bash /init.sh
