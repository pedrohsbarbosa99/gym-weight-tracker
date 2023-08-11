#!/bin/sh

if [ true ]
then
    echo "Waiting for postgres..."

    while ! nc -z db 26257; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"