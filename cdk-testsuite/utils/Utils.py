import os
import re
import time
import subprocess
import pexpect
from avocado import Test
#This is used for decoration purpose only!
dash="===================================================\n"

#This method is used for setting up path according to your platform 
def settingPath(self):
    self.log.debug("Checking your machine OS")
    linux = 'Linux'
    win = "CYGWIN_NT-10.0"
    mac = "Darwin"
    p = subprocess.Popen("uname", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
    if output.strip() == linux:
        self.log.debug("Using Linux yaml parameters")
        var = self.params.get(linux)
        self.log.debug("This is my path variable :" + var)

    elif output.strip() == win:
        self.log.debug("Using win yaml parameters")

        var = self.params.get(win)
        self.log.debug("This is my path variable :" + var)


    elif output.strip() == mac:
        self.log.debug("We are on Mac OS")
        var = self.params.get(mac)
        self.log.debug("This is my variable :" + var)
        self.log.debug("This is my path variable :" + var)

    return var

#This method is doing Vagrant up with the specific provider 
def vagrantUp(self, path,provider):
    self.log.debug(" Vagrant up:: Start")
    self.log.debug("changing path to " + path)
    os.chdir(path)
    paramerters = pexpect.spawn("vagrant up --provider "+self.params.get('vagrant_PROVIDER'))
    paramerters.expect('.*Would you like to register the system now.*', timeout=150)
    paramerters.sendline("y")
    paramerters.expect(".*username.*")
    paramerters.sendline(self.params.get('vagrant_RHN_USERNAME'))
    # paramerters.sendline("naverma@redhat.com")
    paramerters.expect(".*password.*")
    paramerters.sendline(self.params.get('vagrant_RHN_PASSWORD'))
    # paramerters.sendline("*****")
    paramerters.interact()
    paramerters.close()
	#self.log.debug(" Vagrant up:: Exit")

    return 'ok'

#Returning Global status
def global_status(self, vm_name):
    self.log.debug("Checking Global status ::Start")
    p = subprocess.Popen("vagrant global-status |grep " + vm_name + "|awk '{print $4}'", stdout=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
	#self.log.debug("Checking Global status ::Exit")
    return output


def vagrantDestroy(self):
    self.log.info(dash + " vagrant destroy ::Start" + dash)
    p = subprocess.Popen("vagrant destroy", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
	#self.log.info(dash + " vagrant destroy ::Exit" + dash)
    return output


def vagrantSSH(self,command):
    self.log.info(dash + "vagrant SSH :: Start" + dash)
    p = subprocess.Popen("vagrant ssh -c "+command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
	#self.log.info(dash + "vagrant SSH :: Exit" + dash)
    return output


def vagrant_service_manager(self, path, command):
    self.log.debug("vagrant_service_manager module inside Utils:: Start")
    self.log.debug("changing path to " + path)
    os.chdir(path)
    p = subprocess.Popen("vagrant service-manager " + command)
    (output, err) = p.communicate()
    self.log.debug(output)
	#self.log.debug("vagrant_service_manager module inside Utils:: Finish")
    return output


def vagrant_box_add(self):
    self.log.info("Vagrant Box add :: Start")
    p = subprocess.Popen("vagrant box add cdkv2 " + self.params.get('vagrant_BOX_PATH'))
    (output, err) = p.communicate()
    self.log.debug(output)
 #   self.log.info("Vagrant Box add ::Finish")
    return output

def vagrant_box_remove(self):
    self.log.info("Vagrant Box Remove :: Start")
    p = subprocess.Popen("vagrant box remove cdkv2 --force")
    (output, err) = p.communicate()
    self.log.debug(output)
  #  self.log.info("Vagrant Box Remove ::Finish")
    return output

def vagrant_plugin_install(self):
    self.log.info("Vagrant Plugin Install :: Start")
    os.chdir(self.params.get('vagrant_PLUGINS_DIR'))
    os.system("vagrant plugin install ./vagrant-registration-*.gem  ./vagrant-service-manager-*.gem ./vagrant-sshfs-*.gem")
    p = subprocess.Popen("vagrant plugin install ./vagrant-registration-*.gem  ./vagrant-service-manager-*.gem ./vagrant-sshfs-*.gem")
    (output, err) = p.communicate()
    self.log.debug(output)
#    self.log.info("Vagrant Plugin Install ::Finish")

    return output

# This method is for multi windows shell support ,it runs the specific commands in the particalar sheels 
def shell_commands(self, command):
    self.log.info("This method is used because we need to provide support for Powershell , cmd, cygwin, bash,ubuntu")
    if self.params.get('Windows_Shell') == 'powershell':
        operator = '|'
        psxmlgen = subprocess.Popen([r'C:/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe',
                                     'cd ' + self.params.get(
                                         'vagrant_VARGRANTFILE_DIRS') + 'misc/hyperv/rhel-k8s-singlenode-hyperv ' + operator + ' ' + command],
                                    cwd=os.getcwd())
        result = psxmlgen.wait
        time.sleep(20)
        self.log.debug('Suspend result :' + str(result))
    elif self.params.get('Windows_Shell') == 'cmd':
        operator = '&'
        psxmlgen = subprocess.Popen([r'C:/Windows/System32/cmd.exe',
                                     'cd ' + self.params.get(
                                         'vagrant_VARGRANTFILE_DIRS') + 'misc/hyperv/rhel-k8s-singlenode-hyperv ' + operator + ' ' + command],
                                    cwd=os.getcwd())
        result = psxmlgen.wait
        time.sleep(20)
        self.log.debug('Suspend result :' + str(result))





