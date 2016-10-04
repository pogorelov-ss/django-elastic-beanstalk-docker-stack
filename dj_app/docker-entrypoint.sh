#!/usr/bin/env bash

python manage.py migrate  --noinput                # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files
#python manage.py compress --force
ROOT_DIR=$(pwd)
UWSGI_INI_PATH=$ROOT_DIR/uwsgi/

if [ "$1" = 'runserver' ]; then
   echo runserver
   python manage.py runserver 0.0.0.0:8000
elif [ "$1" = 'runserver_plus' ]; then
   echo runserver_plus
   python manage.py runserver_plus 0.0.0.0:8000
else
    echo "**********************************************************************************"
    echo "*^*^*starting UWSGI with $UWSGI_WORKERS workers form $UWSGI_INI_PATH$UWSGI_INI settings file*^*^*"
    echo "**********************************************************************************"
    (cd $UWSGI_INI_PATH && exec uwsgi --ini $UWSGI_INI --processes $UWSGI_WORKERS "$@")
fi