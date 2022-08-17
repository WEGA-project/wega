#!/bin/bash

export COMPOSER_ALLOW_SUPERUSER=1;

apt update
APP_DIR=/var/www/wega-slim
WEGA_SLIM_REPO=https://gitlab.com/ruslan.sfs/wega-slim3.git

apt install apache2 gnuplot gnuplot-nox git libzip-dev curl php libapache2-mod-php php-curl php-mysqli php-pdo-mysql php-zip -y

git clone $WEGA_SLIM_REPO $APP_DIR
cp $APP_DIR/.env.example $APP_DIR/.env
ln -sf $APP_DIR/apache/main.conf /etc/apache2/conf-enabled/

chown -R www-data:www-data $APP_DIR
a2enmod rewrite
systemctl reload apache2

cd $APP_DIR
php ./composer.phar update

echo "ALL INSTALLED"
echo "CHECK CONFIG IN: $APP_DIR/.env"