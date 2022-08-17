# WEGA Slim

\*приложение в разработке!

Для работы нужны как минимум две базы. Первая - основная. В ней будут хранится юзеры, и информация о других базах.
Вторая база устройства. Их может быть много.

Можно создать основную базу с бекапа sql/create-mai-db.sql

В базу нужно добавить записи устройств (имя базы у-ва, название подключения, userid сейчас не важно)

### Docker (apache)

Устанавливаем докер для своей системы по офф мануалу
https://docs.docker.com/engine/install/

И запускаем.

```
docker run --rm \
-e DB_HOST=172.17.0.1 \
-e DB_MAIN_NAME=wega \
-e DB_MAIN_USER=root \
-e DB_DEVICE_USER=root \
-e DB_MAIN_PASS=wega \
-e DB_DEVICE_PASS=wega \
-p 8081:80 \
ruslansfs/wega-slime:0.0.3-apache
```

DB_MAIN - основная база
DB_DEVICE - база данных устройства

Открываем 0.0.0.0:8081

### Установка на работающий wega сервер. (Ubuntu 20.04 LTS lamp)

```
sudo su
wget -O - https://gitlab.com/ruslan.sfs/wega-slim3/-/raw/main/scripts/install-on-wega-lamp-ubuntu-20.sh | bash
```

### Установка скриптом на Debian 11

Ставим cURL если нету

```
apt update && apt install curl -y
```

Качаем скрипт scripts/install-debian.sh с репозитория и запускаем от рута

```
sudo curl https://gitlab.com/ruslan.sfs/wega-slim3/-/raw/main/scripts/install-debian.sh  -o ./install.sh && chmod +x ./install.sh && ./install.sh
```

В процессе так как запуск от рута, composer выдаст предупреждение что он работает от рута, просто жмем
enter.

После открываем файл .env и настраиваем подключения к базе.

Открываем 0.0.0.0:80

### Установка вручную на Debian 11

Решаем куда ставить. Например в /var/www/wega-slim. Дальше - APP_DIR.

###### Устанавливаем зависимости

```
sudo apt update && apt install apache2 gnuplot gnuplot-nox git libzip-dev curl php libapache2-mod-php php-curl php-mysqli php-pdo-mysql php-zip
```

###### Переходим в APP_DIR и клонируем репозиторий

```
cd APP_DIR
git clone https://gitlab.com/ruslan.sfs/wega-slim3.git
```

###### Создаем файл настроек и меняем в нем настройки подключения к базе

```
cp .env.example .env
nano .env
```

###### Создаем ссылку на конфиг для apache2

```
ln -sf /apache/main.conf /etc/apache2/conf-enabled/
```

###### Включаем mod_rewrite для apache2

```
sudo a2enmod rewrite && sudo systemctl reload apache2
```

###### Устанавливаем зависимости php

php ./composer.phar update

###### Все готово, сервис должен быть доступен на порту 80.

##### Также в целях отладки и проверки можно запустить приложение без apache2

```
sudo php -S 0.0.0.0:8080 -t public
```

В этом случае в консоль будет выводится подробный лог.
