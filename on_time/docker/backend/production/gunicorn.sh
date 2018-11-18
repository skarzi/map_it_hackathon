#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


python /app/manage.py migrate --noinput
python /app/manage.py collectstatic --clear --noinput
/usr/local/bin/gunicorn config.wsgi:application -b 0.0.0.0:5000 \
        --workers 4 \
        --threads 12 \
        --name=on_time \
        --access-logfile - \
        --error-logfile - \
        --chdir=/app
