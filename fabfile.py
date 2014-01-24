from fabric.api import *
from fabric.contrib import *
import datetime
import os


def deploy():
  create_web_app_image()


def create_basement_image():
  source_file = './templates/Dockerfile-basement'
  destination_file = './tmp/Dockerfile'

  sudo("mkdir -p ./tmp")
  files.upload_template(source_file, destination_file, mode=0777)

  image = Image("basement", destination_file)
  image.build()
  sudo("rm -rf ./tmp")
  image.image_id()


def create_mysql_image():
  context = { "parent_image_id": Image.image_id("basement")[0], "root_password": "" }
  source_file = './templates/Dockerfile-mysql'
  destination_file = './tmp/Dockerfile'

  sudo("mkdir -p ./tmp")
  files.upload_template(source_file, destination_file, mode=0777)

  image = Image("mysql", destination_file)
  image.build()
  sudo("rm -rf ./tmp")
  image.image_id()


def create_web_basement_image():
  context = { "parent_image_id": Image.image_id("basement")[0] }
  source_file = './templates/Dockerfile-web-server'
  destination_file = './tmp/Dockerfile'

  sudo("mkdir -p ./tmp")
  files.upload_template(source_file, destination_file, context=context, mode=0777)
  files.upload_template("./templates/nginx/default", "./tmp/default", mode=0644)
  files.upload_template("./templates/nginx/default-ssl", "./tmp/default-ssl", mode=0644)

  image = Image("web-basement", destination_file)
  image.build()
  sudo("rm -rf ./tmp")
  image.image_id()


def create_web_app_image():
  context = { "parent_image_id": Image.image_id("web-basement")[0] }
  source_file = './templates/Dockerfile-web-app'
  destination_file = './tmp/Dockerfile'

  sudo("mkdir -p ./tmp")
  files.upload_template(source_file, destination_file, context=context, mode=0777)

  image = Image("web-basement", destination_file)
  image.build()
  sudo("rm -rf ./tmp")
  image.image_id()


def remove_all_images():
  remove_containers_of(repository_name)
  sudo('docker rmi $(sudo docker images -q)')

def remove_images_without_latest_one(repository_name):
  for image_id in Image.image_id_of(repository_name)[1:]:
    sudo("docker rmi %s" % (image_id))

def remove_images(repository_name, tag = None):
  for image_id in Image.image_id_of(repository_name, tag):
    remove_containers_of(repository_name, tag)
    sudo("docker rmi %s" % (image_id))

def remove_all_containers():
  sudo('docker rm $(sudo docker ps -a -q)')


class Image:
  def __init__(self, repository_name, dockerfile_path):
    self.tag = None
    self.repository_name = repository_name
    self.dockerfile_directory = "/".join(dockerfile_path.split("/")[::-1][1:][::-1])

  def build(self):
    self.tag = self.timestamp()
    sudo("docker build -no-cache -t %s:%s %s" % (self.repository_name, self.tag, self.dockerfile_directory))

  def run(self):

  def timestamp(self):
    return datetime.datetime.today().strftime("%Y%m%d%H%M%S")

  def image_id(self):
    return sudo("docker images|grep -E \"^%s\s+%s\"|awk '{print $3}'" % (self.repository_name, self.tag))

  def container_id(self):
    id_array = sudo("docker ps -a|grep %s:%s|awk '{print $1}'" % (self.repository_name, self.tag)).split("\r\n")

    if len(id_array) == 0:
      return None
    elif len(id_array) == 1:
      return id_array[0]
    else:
      return id_array

  # @classmethod
  # def container_ids_of(self, image_id_or_repository_name):
  #   id_array = sudo("docker ps -a|grep %s|awk '{print $1}'" % image_id_or_repository_name).split("\r\n")

  #   if len(id_array) == 0:
  #     return None
  #   elif len(id_array) == 1:
  #     return id_array[0]
  #   else:
  #     return id_array

  @classmethod
  def image_id(self, repository_name, tag = None):
    if tag == None:
      return sudo("docker images|grep -E \"^%s\"|awk '{print $3}'" % (repository_name)).split('\r\n')
    else:
      return sudo("docker images|grep -E \"^%s\s+%s\"|awk '{print $3}'" % (repository_name, tag)).split('\r\n')[0]


def install_docker():
  sudo("sh -c \"wget -qO- https://get.docker.io/gpg | apt-key add -\"")
  sudo("sh -c \"echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list\"")
  sudo("apt-get update -y")
  sudo("apt-get upgrade -y")

  sudo("""
    apt-get install -y \
      sudo \
      man-db \
      wget \
      git \
      nano \
      curl \
      dialog \
      net-tools \
      patch \
      gcc \
      openssl \
      make \
      bzip2 \
      autoconf \
      automake \
      libtool \
      bison
  """)

  sudo("""
    apt-get install -y \
      linux-image-generic-lts-raring \
      linux-headers-generic-lts-raring \
      lxc-docker
  """)
