#!/bin/bash
apt install syslog-ng libdbd-mysql -y
dbpass=`cat db.php|grep "password="|awk -F '\"' '{print $2}'`
echo "password(\""$dbpass"\")" > /etc/syslog-ng/patterndb.d/dbpass
cp wegabox.conf /etc/syslog-ng/conf.d/wegabox.conf
mysql -uroot -p$dbpass < syslog.sql
systemctl restart syslog-ng.service
