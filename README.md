## Preparation

### Configure .ssh/config

if you have not configured ~/.ssh/config to connect vagrant vm, add the following code to that file.

```
Host 192.168.33.12
  User vagrant
  Port 22
  PasswordAuthentication no
  IdentityFile /Users/hdemon/.vagrant.d/insecure_private_key
```

or you can run fabric with the following option every time.

```
fab hoge -h 192.168.33.12 -u vagrant -i ~/.ssh/.vagrant.d/insecure_private_key
```

### Install fabric and start vm

```
pip install fabric
vagrant up
```

### Install docker to the vm

```
fab install_docker -h 192.168.33.12
```

## Usage

First, you should create basement image. This image includes basic packages.
You don't have to build this image in the absence of updating basic packages.

And 'web_basement' image inherits this image's environment. So you can reduce the time to build the basic packages each time. For your information, this image includes the packages to operate web server, like nginx and mysql-client.

```
fab create_basement_image -h 192.168.33.12
fab create_web_basement_image -h 192.168.33.12
```

If you have built these images without incident, you can deploy web app image.

```
fab deploy -h 192.168.33.12
```

The web app image also inherits web basement image. So you can reduce the time for the same reason.
