#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

daphne -b 0.0.0.0 -p 8001 messanger.asgi:application
