#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8000 RoomPriceGenie.wsgi:application --workers=1 --threads=10 --timeout=3600