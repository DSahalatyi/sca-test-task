#!/bin/sh

until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 1
done

python manage.py migrate

python manage.py test
if [ $? -ne 0 ]; then
  echo "Tests failed, exiting..."
  exit 1
fi

python manage.py runserver 0.0.0.0:8000
