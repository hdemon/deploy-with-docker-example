FROM ubuntu

MAINTAINER Masami Yonehara

RUN apt-get update -y
RUN apt-get upgrade -y

# replace PASSWORD
RUN export DEBIAN_FRONTEND=noninteractive;\
  echo mysql-server mysql-server/root_password password PASSWORD | debconf-set-selections;\
  echo mysql-server mysql-server/root_password_again password PASSWORD | debconf-set-selections;\

RUN apt-get install -y \
  mysql-server \
  mysql-client
