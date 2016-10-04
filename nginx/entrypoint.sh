#!/usr/bin/env bash

envsubst '\$ALLOWED_HOST \$NGINX_MAIN_PORT \$NGINX_REDIRECT_PORT' < /etc/nginx/conf.templ/default.conf > /etc/nginx/conf.d/default.conf
exec "$@"