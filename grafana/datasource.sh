#!/bin/bash
pathtoyml="/etc/grafana/provisioning/datasources"

dbpass=`cat /var/WEGA/db.php|grep "password="|awk -F '\"' '{print $2}'`
datasource=`grep my_db /var/WEGA/wegagui/config/*.conf.php|awk -F "\"" '{print $2}'`
IFS=$'\n'
for db in $datasource
do
  unset IFS
  echo "datasources:" >$pathtoyml/$db.yaml
  echo "  - name: $db" >>$pathtoyml/$db.yaml
  echo "    type: mysql" >>$pathtoyml/$db.yaml
  echo "    url: localhost:3306" >>$pathtoyml/$db.yaml
  echo "    database: $db" >>$pathtoyml/$db.yaml
  echo "    user: root" >>$pathtoyml/$db.yaml
  echo "    secureJsonData:" >>$pathtoyml/$db.yaml
  echo "      password: \"$dbpass\"" >>$pathtoyml/$db.yaml


done
unset IFS

systemctl restart grafana-server.service
