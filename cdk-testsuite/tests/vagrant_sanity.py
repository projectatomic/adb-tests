#!/usr/bin/python

from avocado import Test
from avocado.utils import process
import os, pexpect, time

class VagrantSanity(Test):
    def setUp(self):
	self.vagrant_BOX_PATH = self.params.get('vagrant_BOX_PATH')
        self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER', default='')
	self.vagrant_RHN_USERNAME = self.params.get('vagrant_RHN_USERNAME')
	self.vagrant_RHN_PASSWORD = self.params.get('vagrant_RHN_PASSWORD')
	os.chdir(self.vagrant_BOX_PATH)


    def est_vagrant_up(self):
	cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
	self.log.info("Brining up the vagrant box...")
	child = pexpect.spawn ('vagrant up')
	child.expect('.*Would you like to register the system now.*')
	child.sendline ('n')
	self.log.info(child.before)
	time.sleep(60)
	self.test_vagrant_destroy()

    def test_vagrant_up_register(self):
        cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
        self.log.info("Brining up the vagrant box and registering to RHN...")
        child = pexpect.spawn ('vagrant up')
        child.expect('.*Would you like to register the system now.*')
        child.sendline ('y')
        child.expect('.*username.*')
        child.sendline('self.vagrant_RHN_USERNAME')
        child.expect('.*password.*')
        child.sendline('self.vagrant_RHN_PASSWORD')
        self.log.info(child.before)


    def test_vagrant_status(self):
	cmd = "vagrant global-status | grep '%s' | awk '{print $4}'" %(self.vagrant_BOX_PATH.strip("/"))
	self.log.info("Checking the status of the vagrant box...")
        out = process.run(cmd, shell=True)
        self.log.debug(out)
	if out.stdout.strip('\n') in ["preparing", "running"]:
	    self.log.info("The vagrant Box is running fine")
	    self.assertTrue(out.stdout is "preparing" or "running")
	else:
	    self.log.info("The vagrant Box is NOT running fine")
	    self.assertFalse(out.stdout is not None)

    def test_ssh_into_box(self):
	cmd = "vagrant ssh -c 'uname'"
        self.log.info("Checking the ssh access into the vagrant box...")
        out = process.run(cmd, shell=True)
        self.log.debug(out)
        self.assertEqual("Linux\r\n", out.stdout)


    def test_vagrant_suspend(self):
	cmd = "vagrant suspend"
        self.log.info("Suspending the vagrant box...")
        out = process.run(cmd, shell=True)
        self.log.debug(out)
	self.assertEqual("==> default: Suspending domain...\n", out.stdout)
	self.assertNotIn("default: Domain is not created. Please run `vagrant up` first.", out.stdout)


    def test_vagrant_resume(self):
        cmd = "vagrant resume"
        self.log.info("Resuming the vagrant box...")
        out = process.run(cmd, shell=True)
        self.log.debug(out)
	self.assertEqual("==> default: Resuming domain...\n", out.stdout)
	self.assertNotIn("==> default: Domain is not created. Please run `vagrant up` first.\n", out.stdout)

    def est_vagrant_reload(self):
        cmd = "vagrant reload"
        self.log.info("Reloading the vagrant box...")
        out = process.run(cmd, shell=True)
        self.log.debug(out)
        self.assertNotIn("==> default: Domain is not created. Please run `vagrant up` first.\n", out.stdout)


    def test_vagrant_destroy(self):
        cmd = "vagrant destroy -f"
        self.log.info("Destroying the vagrant box...")
        out = process.run(cmd, shell=True)
        self.log.debug(out)
        self.assertIn("==> default: Removing domain...\n", out.stdout)
        self.assertNotIn("==> default: Domain is not created. Please run `vagrant up` first.\n", out.stdout)


