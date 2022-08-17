#!/bin/bash
DB_FILES_DIR=/var/WEGA/wegagui/config/*.conf.php
DB_PASS=$(echo "<?php include '/var/WEGA/db.php'; echo \$password;" | /usr/bin/php)
MAIN_DB_NAME=wega
MYSQL=`which mysql`

Q_CREATE_DB="CREATE DATABASE IF NOT EXISTS $MAIN_DB_NAME;"
Q_USE="use $MAIN_DB_NAME;"
Q_CREATE_DEVICES="CREATE TABLE devices (id int NOT NULL AUTO_INCREMENT,db varchar(255) NOT NULL,name varchar(255) NOT NULL,userid int NOT NULL,PRIMARY KEY (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
Q_INSERT="INSERT INTO devices (db, name, userid) VALUES"

echo "Create db $MAIN_DB_NAME"

SQL="$Q_CREATE_DB $Q_USE $Q_CREATE_DEVICES"

echo "SQL: $SQL"

$MYSQL -uroot -p$DB_PASS -e "$SQL"

echo DB PASS: $DB_PASS
echo MAIN DB NAME: $MAIN_DB_NAME

for file in $DB_FILES_DIR
do
    if [ -f "$file" ]
    then
        DEVICE_DB_NAME="$(basename $file .conf.php)";
        echo INSERT $DEVICE_DB_NAME;
        
        Q_VALUES="('$DEVICE_DB_NAME','$DEVICE_DB_NAME',1);";
        
        SQL="$Q_USE $Q_INSERT $Q_VALUES";
        
        echo SQL: $SQL;
        
        $MYSQL -uroot -p$DB_PASS -e "$SQL";
    fi
done
