#!/usr/bin/env sh
gpasswd -a application tty

touch                      \
  /var/run/supervisord.pid \
  /var/run/application.pid \
  /var/run/oauth.pid       \
 && chown application:     \
  /var/run/supervisord.pid \
  /var/run/application.pid \
  /var/run/oauth.pid

/usr/local/bin/supervisord -c /etc/supervisord.conf
