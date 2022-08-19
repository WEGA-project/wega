#!/bin/bash
echo 'starting'
set -xe
cd /var/WEGA/wega-hpg/
source /var/WEGA/wega-hpg/venv/bin/activate
var/WEGA/wega-hpg/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5003 project.wsgi:application