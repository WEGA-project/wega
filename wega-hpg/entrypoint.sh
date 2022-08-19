echo 'starting'
set -xe
python manage_prod.py collectstatic --noinput
python manage_prod.py migrate  --noinput
python runserver.py --port 5003