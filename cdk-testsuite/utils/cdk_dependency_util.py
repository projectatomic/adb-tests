import time
from avocado import Test
import subprocess
import os

def platform_verification(self):
    self.log.info("Checking which operating system are you using::")
    p = subprocess.Popen("uname -a", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    self.log.debug(output)
    if "Linux" in output:
        self.log.debug("Operating System name is ::  " + output)
        return "Linux"
    elif "CYGWIN" in output:
        self.log.debug("Operating System name is ::  " + output)
        return "CYGWIN  "
    elif "Darwin" in output:
        self.log.debug("Operating System name is ::  " + output)
        return "Darwin"

def vagrant_installation(self,machine=None,sudopassword=None):
    self.log.info("Downloading Vagrant on Machine ::" +machine)
    if machine == "Linux":
        self.log.info("Vagrant binary downloading on "+machine)
        self.log.info("echo "+str(sudopassword)+" | sudo -S dnf install vagrant -y")
        os.system("echo "+str(sudopassword)+" | sudo -S dnf install vagrant -y")
    elif machine == "CYGWIN":
        self.log.info("Vagrant binary downloading on " + machine)
        os.system("wget https://releases.hashicorp.com/vagrant/1.8.4/vagrant_1.8.4.msi")
        os.system('msiexec.exe /a vagrant_1.8.4.msi')
        time.sleep(30)
    elif machine == "Darwin":
        self.log.info("Vagrant binary downloading on " + machine)
        os.system("wget https://releases.hashicorp.com/vagrant/1.8.4/vagrant_1.8.4.msi")
        os.system('msiexec.exe /a vagrant_1.8.4.msi')
        time.sleep(30)



