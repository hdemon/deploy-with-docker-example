#!/bin/sh

MYSQL_PASSWORD=app

# mysql
export DEBIAN_FRONTEND=noninteractive
echo mysql-server mysql-server/root_password password $MYSQL_PASSWORD | debconf-set-selections
echo mysql-server mysql-server/root_password_again password $MYSQL_PASSWORD | debconf-set-selections

apt-get install -y \
  mysql-server \
  mysql-client
