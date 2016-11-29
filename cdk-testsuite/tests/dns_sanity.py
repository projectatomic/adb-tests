#!/usr/bin/python

from avocado import Test
from avocado.utils import process
import os, re, pexpect, vagrant, platform, sys

class VagrantSanity(Test):
    def setUp(self):
	self.vagrant_VAGRANTFILE_DIR = self.params.get('vagrant_VAGRANTFILE_DIR')
	self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER')
	self.vagrant_RHN_USERNAME = self.params.get('vagrant_RHN_USERNAME')
	self.vagrant_RHN_PASSWORD = self.params.get('vagrant_RHN_PASSWORD')
	self.platform = platform.system()
	self.sudo_PASSWORD = self.params.get('sudo_PASSWORD')
	self.suspended_state = ["paused", "saved", "shutoff"]
	self.halt_state = ["off", "shutoff", "poweroff"]
	self.registration_required = self.credentials_exported = False
	self.vagrant_file = os.path.join(self.vagrant_VAGRANTFILE_DIR, "Vagrantfile") 
	if os.path.exists(self.vagrant_file) and os.path.getsize(self.vagrant_file) > 0:
	    self.v = vagrant.Vagrant(self.vagrant_VAGRANTFILE_DIR)
	    os.chdir(self.vagrant_VAGRANTFILE_DIR)
	    fd = open(self.vagrant_file, 'r')
	    data = fd.read()
	    if re.search(r'REQUIRED_PLUGINS = .* (vagrant-registration) .*',data):
	        self.registration_required = True
	    if os.getenv('SUB_USERNAME') and os.getenv('SUB_PASSWORD'):
		self.credentials_exported = True	
	else:
	    print "Please check the vagrant file and re-run the test"
	    sys.exit(1)

    def test_connection_host_to_guest(self):
        ''' Testing connection from host to guest '''
        self.log.info("Trying host to guest ping")
        guest_ip = self.v.hostname()
        self.log.info(guest_ip)
        cmd = "ping -c 5 " + guest_ip
        child = pexpect.spawn (cmd)
        index = child.expect (["5 received", "0 received", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        if index==0:
            self.log.info("ping ok")
        else:
            self.fail("O packets received")

    def test_dns_from_guest(self):
        ''' Testing dns connection from guest to outside network '''
        self.log.info("Checking dns from guest to outside network")
        cmd = "vagrant ssh -c 'ping -c 5 twitter.com'"
        child = pexpect.spawn (cmd)
        guest_index = child.expect (["5 received", "0 received", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        cmd = "ping -c 5 twitter.com"
        child = pexpect.spawn (cmd)
        host_index = child.expect (["5 received", "0 received", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
        if host_index==0 and guest_index==0:
            self.log.info("Twitter is accessible from both host box.")
	elif guest_index==0:
            self.fail("Guest ping to Twitter - ok, host ping to Twitter - failed")
        elif host_index==0:
            self.fail("Guest ping to Twitter - failed, host ping to Twitter - ok")
        else:
            self.fail("Both guest and host are unable to access Twitter")


