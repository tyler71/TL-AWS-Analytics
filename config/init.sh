#!/usr/bin/env sh
gpasswd -a application tty

for pid in \
  /var/run/supervisord.pid
do
  touch "$pid"
  chown application: "$pid"
done

/usr/local/bin/supervisord -c /etc/supervisord.conf
