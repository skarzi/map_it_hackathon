#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

celery flower \
    --app=apps.taskapp \
    --broker="${CELERY_BROKER_URL}" 
