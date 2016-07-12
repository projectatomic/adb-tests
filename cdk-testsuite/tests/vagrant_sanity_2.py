#!/usr/bin/python

from avocado import Test
from avocado.utils import process
import os, re, time, pexpect, vagrant

class VagrantSanity(Test):
    def setUp(self):
	self.vagrant_BOX_PATH = self.params.get('vagrant_BOX_PATH')
        self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER', default='')
	self.vagrant_RHN_USERNAME = self.params.get('vagrant_RHN_USERNAME')
	self.vagrant_RHN_PASSWORD = self.params.get('vagrant_RHN_PASSWORD')
	os.chdir(self.vagrant_BOX_PATH)
	self.v = vagrant.Vagrant(self.vagrant_BOX_PATH)


    def vagrant_status(self):
        self.log.info("Checking the status of the vagrant box...")
        out = self.v.status()
        state = re.search(r"state='(.*)',", str(out) ).group(1)
        self.log.info("State of the vagrant box is %s" %(state))
        return state


    def test_vagrant_up(self):
	self.log.info("Destroying any old vagrant box...")
	self.test_vagrant_destroy()
	cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
	self.log.info("Brining up the vagrant box...")
	child = pexpect.spawn ('vagrant up')
	child.expect('.*Would you like to register the system now.*',timeout=250)
	child.sendline ('n')
	#self.log.info(child.before)
	time.sleep(60)
	self.vagrant_status()
	self.test_vagrant_destroy()

    def test_vagrant_up_register(self):
        cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
        self.log.info("Brining up the vagrant box and registering to RHN...")
        child = pexpect.spawn ('vagrant up')
        child.expect('.*Would you like to register the system now.*', timeout=250)
        child.sendline ('y')
        child.expect('.*username.*')
        child.sendline('self.vagrant_RHN_USERNAME')
        child.expect('.*password.*')
        child.sendline('self.vagrant_RHN_PASSWORD')
        #self.log.info(child.before)
	self.vagrant_status()
  
    def test_ssh_into_box(self):
	cmd = "vagrant ssh -c 'uname'"
        self.log.info("Checking the ssh access into the vagrant box...")
        out = process.run(cmd, shell=True)
        self.assertEqual("Linux\r\n", out.stdout)


    def test_vagrant_suspend(self):
        self.log.info("Suspending the vagrant box...")
        self.v.suspend()
        out = self.vagrant_status()
	#self.assertTrue(out is "paused" or "saved")


    def test_vagrant_resume(self):
        self.log.info("Resuming the vagrant box...")
        self.v.resume()
        out = self.vagrant_status()
	self.assertEqual("running", out)


    def test_vagrant_halt(self):
        self.log.info("Halting the vagrant box...")
        self.v.halt()
        out = self.vagrant_status()
        self.assertTrue(out is "shutoff" or "poweroff")


    def test_vagrant_reload(self):
        self.log.info("Reloading the vagrant box...")
        self.v.reload()
	out = self.vagrant_status()
        self.assertEqual("running", out)


    def test_vagrant_destroy(self):
        self.log.info("Destroying the vagrant box...")
        self.v.destroy()
        out = self.vagrant_status()
        self.assertEqual("not_created", out)

