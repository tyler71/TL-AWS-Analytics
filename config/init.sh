#!/usr/bin/env sh

# Fix /dev/stdout permissions error
gpasswd -a application tty
chmod o+w /dev/stdout /dev/stderr

# Fix supervisor pid permissions error
for pid in \
  /var/run/supervisord.pid
do
  touch "$pid"
  chown application: "$pid"
done

/usr/local/bin/supervisord -c /etc/supervisord.conf
