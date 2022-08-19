#!/bin/bash

echo 'starting'
set -xe
cd /var/WEGA/wega-hpg/
source /var/WEGA/wega-hpg/venv/bin/activate
python manage_prod.py collectstatic --noinput
python manage_prod.py migrate  --noinput
python runserver.py --port 5003