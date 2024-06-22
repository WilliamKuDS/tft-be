#!/bin/sh

if [ "$DJANGO_ENV" = "development" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn --bind 0.0.0.0:8000 tft_django.wsgi
fi
