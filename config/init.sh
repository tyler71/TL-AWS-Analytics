#!/usr/bin/env sh
gpasswd -a application tty

chmod o+w /dev/stdout /dev/stderr

for pid in \
  /var/run/supervisord.pid
do
  touch "$pid"
  chown application: "$pid"
done

/usr/local/bin/supervisord -c /etc/supervisord.conf
