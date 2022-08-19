#!/bin/bash

echo "#############################"
echo "Do you want to update the OS:"
echo "#############################"
read -p "[yes/no]: " OS_UPDATE

WEGA_USER_NAME="wega"

apt update
if [[ "$OS_UPDATE" == 'yes' ]]
then
  apt dist-upgrade -y
fi

echo "#############################"
echo "###### Installing Soft ######"
echo "#############################"
printf "\n"
sleep 5

apt install lamp-server^ php-curl gnuplot-nox git curl syslog-ng libdbd-mysql -y

echo "##############################"
echo "######## MySQL config ########"
echo "##############################"
printf "\n"
sleep 5

MYSQL=`which mysql`
MYSQL_PSWD=$(openssl rand -hex 12)

Q1="ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_PSWD';"
Q2="SET GLOBAL log_bin_trust_function_creators = 1;"
Q3="FLUSH PRIVILEGES;"
SQL="${Q1}${Q2}${Q3}"

$MYSQL -uroot -e "$SQL"

echo "log-bin-trust-function-creators = 1" >> /etc/mysql/mysql.conf.d/mysqld.cnf

systemctl restart mysql

echo "#############################"
echo "###### Clone WEGA repo ######"
echo "#############################"
printf "\n"
sleep 5

git clone https://github.com/WEGA-project/WEGA.git /var/WEGA

# Syslog config 
cp /var/WEGA/wegabox.conf /etc/syslog-ng/conf.d/wegabox.conf
echo "password(\""$MYSQL_PSWD"\")" > /etc/syslog-ng/patterndb.d/dbpass
mysql -uroot -p$MYSQL_PSWD < /var/WEGA/syslog.sql

systemctl restart syslog-ng

echo "###################################"
echo "###### Configure WEGA server ######"
echo "###################################"
printf "\n"
sleep 5

ln -s /var/WEGA/apache/WEGA-auth.conf /etc/apache2/conf-enabled/
ln -s /var/WEGA/apache/wega-api.conf /etc/apache2/conf-enabled/
cp /var/WEGA/example.db.php /var/WEGA/db.php
sed -i "s/DATABASE_PASSWORD/$MYSQL_PSWD/g" /var/WEGA/db.php 

chown -R www-data:www-data /var/WEGA

# WEGA API secret config
cp /var/WEGA/wega-api/wegabox.php.example /var/WEGA/wega-api/wegabox.php
WEGA_API_TOKEN=$(openssl rand -hex 18)
sed -i "s/adab637320e5c47624cdd15169276981/$WEGA_API_TOKEN/g"  /var/WEGA/wega-api/wegabox.php


# WEGA UI config
WEGA_UI_PSWD=$(openssl rand -hex 10)
cp /var/WEGA/wegagui/config/example/example.conf.php /var/WEGA/wegagui/config/esp32wega.conf.php 
htpasswd -b -c /etc/apache2/.htpasswd $WEGA_USER_NAME $WEGA_UI_PSWD

systemctl reload apache2

echo "#############################"
echo "###### Check WEGA-API  ######"
echo "#############################"
printf "\n"
sleep 5

# Check DB connection and post data
curl -X POST "http://127.0.0.1/wega-api/wegabox.php?auth=$WEGA_API_TOKEN&db=esp32wega&RootTemp=25&AirTemp=25&AirHum=50"
printf "\n"
printf "\n"

# POST config info
printf "\n"
echo "############################################################"
echo "                _       __ ______ ______ ___ "
echo "               | |     / // ____// ____//   |"
echo "               | | /| / // __/  / / __ / /| |"
echo "               | |/ |/ // /___ / /_/ // ___ |"
echo "               |__/|__//_____/ \____//_/  |_|"
printf "\n"
echo "           _____  ______ ____  _    __ ______ ____ "
echo '          / ___/ / ____// __ \| |  / // ____// __ \'
echo '          \__ \ / __/  / /_/ /| | / // __/  / /_/ /'
echo "         ___/ // /___ / _, _/ | |/ // /___ / _, _/ "
echo "        /____//_____//_/ |_|  |___//_____//_/ |_|  "
echo "############################################################"
printf "\n\n"
echo "#######################"
echo "### WEGA SERVER URL ###"
echo "#######################"
if [[  "$(curl -s ipinfo.io | grep -o Amazon)" == "Amazon" ]]
then
    AWS_PUBLIC_IP=$(curl -s 'http://169.254.169.254/latest/meta-data/public-ipv4')
    echo 'WEGA_SERVER_IP: http://'$AWS_PUBLIC_IP'/wega'
else
    echo "WEGA_SERVER_IP: http://$(hostname -I | sed -e "s/\s$//g")/wega"
fi

echo "WEGA_UI_USERNAME: $WEGA_USER_NAME"
echo "WEGA_UI_PASSWORD: $WEGA_UI_PSWD"

printf "\n"
printf "\n"
echo "######################"
echo "### WEGABOX config ###"
echo "######################"
if [[  "$(curl -s ipinfo.io | grep -o Amazon)" == "Amazon" ]]
then
    AWS_PUBLIC_IP=$(curl -s 'http://169.254.169.254/latest/meta-data/public-ipv4')
    echo 'String wegaapi  = "http://'$AWS_PUBLIC_IP'/wega-api/wegabox.php";'
    echo '#define SYSLOG_SERVER "'$AWS_PUBLIC_IP'"'
else
    SERVER_IP=$(hostname -I | sed -e "s/\s$//g"|awk '{print $1}')
    echo 'String wegaapi  = "http://'$SERVER_IP'/wega-api/wegabox.php";'
    echo '#define SYSLOG_SERVER "'$SERVER_IP'"'
fi
echo 'String wegaauth = "'$WEGA_API_TOKEN'";'
echo 'String wegadb   = "esp32wega";'
