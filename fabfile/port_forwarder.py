from fabric.api import *
from fabric.contrib import *


class PortForwarder:
  @classmethod
  # def map(self, host, mapped_to_container):
  #   source_file = './templates/redir.sh'
  #   destination_file = './tmp/redir.sh'
  #   print host

  #   print mapped_to_container
  #   files.upload_template(source_file, destination_file, context={"host":host, "mapped_to_container":mapped_to_container}, mode=0777)

  #   sudo("./tmp/redir")

  def map(self, host, mapped_to_container):
    command = "redir --lport %s --cport %s &" % (host, mapped_to_container)
    sudobg(command)

    # run("nohup %s >& /dev/null < /dev/null &" % command)

    # sudo("nohup %s > /dev/null 2>&1 &" % command)
    # sudo("nohup %s >& /dev/null < /dev/null &" % command)

  @classmethod
  def kill(self):
    for pid in self.current_pids():
      try:
        sudo("kill -kill %s" % pid)
      except:
        print

  @classmethod
  def current_pids(self):
    print sudo("ps aux|grep 'sudo redir'")
    return sudo("ps aux|grep 'sudo redir'| awk '{ print $2 }'").split("\r\n")

def sudobg(cmd, sockname="dtach"):
  return sudo('dtach -n `mktemp -u /tmp/%s.XXXX` %s'  % (sockname,cmd))
