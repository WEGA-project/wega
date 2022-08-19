echo "#######################WEGA-WEB-HPG#######################"
echo "Create database"
MYSQL=`which mysql`
DB_PASS=$(echo "<?php include '/var/WEGA/db.php'; echo \$password;" | /usr/bin/php)
echo "Create wega-hpg db name: $MAIN_DB_NAME"
SQL="CREATE DATABASE IF NOT EXISTS wegacalc;"
$MYSQL -uroot -p$DB_PASS -e "$SQL"
echo "Install python"
apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends python3-pip python3-venv \
build-essential libssl-dev libffi-dev python3-dev  libmysqlclient-dev libev-dev python3-wheel
deactivate
rm -R /var/WEGA/wega-hpg/venv
python3 -m venv /var/WEGA/wega-hpg/venv
source /var/WEGA/wega-hpg/venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt