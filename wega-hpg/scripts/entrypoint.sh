echo 'starting'
set -xe
python manage.py collectstatic --noinput
python manage_prod.py migrate  --noinput
python manage_docker_bjoern.py --port 5003  & python manage_docker_bjoern.py --port 5004