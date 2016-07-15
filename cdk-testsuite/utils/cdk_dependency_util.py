import time
from avocado import Test
import subprocess
import imp
import os
Utils = imp.load_source('Utils', '../utils/Utils.py')

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
        self.log.info("echo "+str(sudopassword)+" | sudo -S yum install vagrant -y")
        os.system("echo "+str(sudopassword)+" | sudo -S yum install vagrant -y")
    elif "CYGWIN" in machine:
        self.log.info("Vagrant binary downloading on " + machine)
        if not os.path.isfile('./vagrant_1.8.4.msi'):
            self.log.info('wget https://releases.hashicorp.com/vagrant/1.8.4/vagrant_1.8.4.msi')
            p = subprocess.Popen('wget https://releases.hashicorp.com/vagrant/1.8.4/vagrant_1.8.4.msi', stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            self.log.debug(output)
        else:
            os.system('msiexec.exe /a vagrant_1.8.4.msi')
            time.sleep(30)
            self.log.info('')
    elif "Darwin" in machine:
        self.log.info("Vagrant binary downloading on " + machine)
        self.log.info("Under construction!!")
        

def enable_virtualization(self,machine=None,sudopassword=None,sub_username=None,sub_password=None):
    self.log.info("Enableing virtualization on machine "+machine)
    if machine == "Linux":
        p = subprocess.Popen("lsb_release -a", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        self.log.debug(output)
        if "Fedora" in output:
            self.log.info("The linux machine is "+str(output))
            self.log.info("echo "+str(sudopassword)+" | sudo -S dnf -y update")
            os.system("echo "+str(sudopassword)+" | sudo -S dnf -y update")
            ## Enable Virtualization 
            self.log.info("echo "+str(sudopassword)+" | sudo -S dnf install @Virtualization")
            os.system("echo "+str(sudopassword)+" | sudo -S dnf install @Virtualization")
            ### Launch the libvirt daemon and configure it to start at boot.
            self.log.info("echo "+str(sudopassword)+" | sudo -S systemctl start libvirtd")
            os.system("echo "+str(sudopassword)+" | sudo -S systemctl start libvirtd")
            self.log.info("echo "+str(sudopassword)+" | sudo -S systemctl enable libvirtd")
            os.system("echo "+str(sudopassword)+" | sudo -S systemctl enable libvirtd")

            ### Install Vagrant and other required packages, including the vagrant-registration and vagrant-libvirt plugins:
            self.log.info("echo "+str(sudopassword)+" | sudo -S dnf install vagrant vagrant-libvirt vagrant-libvirt-doc vagrant-registration rubygem-ruby-libvirt")
            os.system("echo "+str(sudopassword)+" | sudo -S dnf install vagrant vagrant-libvirt vagrant-libvirt-doc vagrant-registration rubygem-ruby-libvirt")
            ### vagrant group to control VMs through libvirt
            self.log.info("cp /usr/share/vagrant/gems/doc/vagrant-libvirt-0.0.*/polkit/10-vagrant-libvirt.rules /etc/polkit-1/rules.d")
            os.system("cp /usr/share/vagrant/gems/doc/vagrant-libvirt-0.0.*/polkit/10-vagrant-libvirt.rules /etc/polkit-1/rules.d")
            ### Restart the libvirt and PolicyKit services for the changes to take effect:
            self.log.info("echo "+str(sudopassword)+" | sudo -S  systemctl restart libvirtd")
            os.system("echo "+str(sudopassword)+" | sudo -S  systemctl restart libvirtd")
            self.log.info("echo "+str(sudopassword)+" | sudo -S systemctl restart polkit")
            os.system("echo "+str(sudopassword)+" | sudo -S systemctl restart polkit")
            ### check vagrant global-status after that 

        elif "RedHat" in output:
            self.log.info("The linux machine is "+str(output))
            ###  Adding Redhat subscription 
            
            p = subprocess.Popen("subscription-manager register --auto-attach --username="+sub_username+" --password="+sub_password, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            self.log.debug(output)

            p1 = subprocess.Popen("subscription-manager repos --enable rhel-variant-rhscl-7-rpms", stdout=subprocess.PIPE, shell=True)
            (output1, err1) = p1.communicate()
            self.log.debug(output1)

            p2 = subprocess.Popen("subscription-manager repos --enable rhel-7-variant-optional-rpms", stdout=subprocess.PIPE, shell=True)
            (output2, err2) = p2.communicate()
            self.log.debug(output2)

            p3 = subprocess.Popen("yum-config-manager --add-repo=http://mirror.centos.org/centos-7/7/sclo/x86_64/sclo/", stdout=subprocess.PIPE, shell=True)
            (output3, err3) = p3.communicate()
            self.log.debug(output3)

            p4 = subprocess.Popen("echo \"gpgcheck=0\" >> /etc/yum.repos.d/mirror.centos.org_centos-7_7_sclo_x86_64_sclo_.repo", stdout=subprocess.PIPE, shell=True)
            (output4, err4) = p4.communicate()
            self.log.debug(output4)

            self.log.info("echo "+str(sudopassword)+" | sudo -S  yum -y update")
            os.system("echo "+str(sudopassword)+" | sudo -S  yum -y update")
            ## Enable Virtualization 
            self.log.info("echo "+str(sudopassword)+" | sudo -S yum groupinstall -y \"Virtualization Host\"")
            os.system("echo "+str(sudopassword)+" | sudo -S yum groupinstall -y \"Virtualization Host\"")
            ### Launch the libvirt daemon and configure it to start at boot.
            self.log.info("echo "+str(sudopassword)+" | sudo -S dnf install @Virtualization")
            os.system("echo "+str(sudopassword)+" | sudo -S dnf install @Virtualization")
            self.log.info("echo "+str(sudopassword)+" | sudo -S systemctl start libvirtd")
            os.system("echo "+str(sudopassword)+" | sudo -S systemctl start libvirtd")
            self.log.info("echo "+str(sudopassword)+" | sudo -S systemctl enable libvirtd")
            os.system("echo "+str(sudopassword)+" | sudo -S systemctl enable libvirtd")
            ### Install Vagrant and other required packages, including the vagrant-registration and vagrant-libvirt plugins:
            self.log.info("echo "+str(sudopassword)+" | sudo -S yum install sclo-vagrant1 sclo-vagrant1-vagrant-libvirt sclo-vagrant1-vagrant-libvirt-doc sclo-vagrant1-vagrant-registration")
            os.system("echo "+str(sudopassword)+" | sudo -S yum install sclo-vagrant1 sclo-vagrant1-vagrant-libvirt sclo-vagrant1-vagrant-libvirt-doc sclo-vagrant1-vagrant-registration")
    
            ### vagrant group to control VMs through libvirt
            self.log.info("cp /opt/rh/sclo-vagrant1/root/usr/share/vagrant/gems/doc/vagrant-libvirt-*/polkit/10-vagrant-libvirt.rules /etc/polkit-1/rules.d")
            os.system("cp /opt/rh/sclo-vagrant1/root/usr/share/vagrant/gems/doc/vagrant-libvirt-*/polkit/10-vagrant-libvirt.rules /etc/polkit-1/rules.d")
            ### Restart the libvirt and PolicyKit services for the changes to take effect:
            self.log.info("echo "+str(sudopassword)+" | sudo -S  systemctl restart libvirtd")
            os.system("echo "+str(sudopassword)+" | sudo -S  systemctl restart libvirtd")
            self.log.info("echo "+str(sudopassword)+" | sudo -S systemctl restart polkit")
            os.system("echo "+str(sudopassword)+" | sudo -S systemctl restart polkit")
            ### check vagrant global-status after that
        else:
            self.log.info("Something went wrong !!")

    elif "CYGWIN" in machine:
        self.log.info(" This is an Windows machine with complete name ::  " + machine)
        ## Utils.sh_cmd() Continue.. with hyper - V if enabled

    elif "Darwin" in machine:
        self.log.info("Vagrant binary downloading on " + machine)
        self.log.info("Under construction!!")




def virtualbox_installation(self,machine=None,sudopassword=None):
    self.log.info("Downloading Vagrant on Machine ::" +machine)
    if machine == "Linux":
        # Not implimented yet
        self.log.info("virtualbox this part is already done in Installing virtualization ::s "+machine)
        
    elif "CYGWIN" in machine:
        # Not implimented yet
        self.log.info("virtualbox binary should be already present on your :: " + machine)

    elif "Darwin" in machine:
        # Not implimented yet
        self.log.info("virtualbox binary should be already present on your :: " + machine)




