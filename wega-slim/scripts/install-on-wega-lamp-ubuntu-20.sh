#!/bin/bash
WEGA_ROOT_PATH=/var/WEGA
#Need for not show root access warning where composer run.
export COMPOSER_ALLOW_SUPERUSER=1

#Parse WEGA constants.
WEGA_SLIM_INSTALL_DIR=/var/WEGA/wega-slim
DB_PASS=$(echo "<?php include '$WEGA_ROOT_PATH/db.php'; echo \$password;" | /usr/bin/php)
DB_HOST=$(echo "<?php include '$WEGA_ROOT_PATH/db.php'; echo \$dbhost;" | /usr/bin/php)
DB_PASS=$(echo "<?php include '/var/WEGA/db.php'; echo \$password;" | /usr/bin/php)
#Install deps for wega-sim
apt update -y
apt install php-pdo-mysql php-zip -y

#Get poject files
#git clone https://gitlab.com/ruslan.sfs/wega-slim3.git $WEGA_SLIM_INSTALL_DIR

#Setup project
cd $WEGA_SLIM_INSTALL_DIR
cp .env.example .env
chmod +x ./scripts/*

#Insert config constants
sed -i "s/^DB_MAIN_PASS\=\".*\"/DB_MAIN_PASS=\"$DB_PASS\"/g" .env
sed -i "s/^DB_DEVICE_PASS\=\".*\"/DB_DEVICE_PASS=\"$DB_PASS\"/g" .env
sed -i "s/^DB_HOST\=\".*\"/DB_HOST=\"$DB_HOST\"/g" .env

#Install wega-slim dependencies
#php ./composer.phar update

#Set right file perms
chown -R www-data:www-data $WEGA_SLIM_INSTALL_DIR

#Create apache2 config for wega-slim
ln -sf $WEGA_SLIM_INSTALL_DIR/apache/embedded-slim-wega.conf /etc/apache2/conf-enabled/

#Enable apache2 rewirite module
a2enmod rewrite

#Restart apache2
systemctl restart apache2

#Create main db

. $WEGA_SLIM_INSTALL_DIR/scripts/import-maindb-from-wega.sh

echo "SUCCESS. Now tyr open yourserver:port/wega-slim"
echo "Sql functions and Fields associations must be configured in main wega interface first!"



