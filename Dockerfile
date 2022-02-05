FROM python:3.10-slim AS build

RUN apt-get update \
 && apt-get -y install g++ \
 && rm -r /var/lib/apt/lists/*

COPY ./packages ./
RUN python -m pip install $(echo $(tr '\n' ' ' < ./packages))

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

USER application
WORKDIR /app

CMD bash ./main.sh

