#!/usr/bin/python

from avocado import Test
from avocado.utils import process
import os, re, time, pexpect, vagrant

class VagrantSanity(Test):
    def setUp(self):
	self.vagrant_VAGRANTFILE_DIR = self.params.get('vagrant_VAGRANTFILE_DIR')
        self.vagrant_PROVIDER = self.params.get('vagrant_PROVIDER', default='')
	self.vagrant_RHN_USERNAME = self.params.get('vagrant_RHN_USERNAME')
	self.vagrant_RHN_PASSWORD = self.params.get('vagrant_RHN_PASSWORD')
	os.chdir(self.vagrant_VAGRANTFILE_DIR)
	self.v = vagrant.Vagrant(self.vagrant_VAGRANTFILE_DIR)


    def vagrant_status(self):
    	''' checks status of vagrant box and returns the state '''
        self.log.info("Checking the status of the vagrant box...")
        out = self.v.status()
        state = re.search(r"state='(.*)',", str(out) ).group(1)
        self.log.info("State of the vagrant box is %s" %(state))
        return state


    def test_vagrant_up(self):
    	''' destroy old box and bring up a the vagrant box and finally destroy '''
	self.log.info("Destroying old vagrant box, if any...")
	self.test_vagrant_destroy()
	#cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
	self.log.info("Brining up the vagrant box...")
	child = pexpect.spawn ('vagrant up')
	child.expect('.*Would you like to register the system now.*', timeout=300)
	child.sendline ('n')
	time.sleep(60)
	out = self.vagrant_status()
	self.assertEqual("running", out)
	self.test_vagrant_destroy()

    def test_vagrant_up_register(self):
    	''' vagrant up with registration to RHN '''
        #cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
        self.log.info("Brining up the vagrant box and registering to RHN...")
        os.environ["SUB_USERNAME"] = self.vagrant_RHN_USERNAME
	os.environ["SUB_PASSWORD"] = self.vagrant_RHN_PASSWORD
	self.v.up()
	out = self.vagrant_status()
	self.assertEqual("running", out)


    def test_ssh_into_box(self):
    	''' test ssh into the vagrant box '''
	cmd = "vagrant ssh -c 'uname'"
        self.log.info("Checking the ssh access into the vagrant box...")
        out = process.run(cmd, shell=True)
        self.assertEqual("Linux\r\n", out.stdout)
	self.log.info("ssh access into the vagrant box is successful...")

    def test_vagrant_suspend(self):
    	''' test to suspend the vagrant box '''
        self.log.info("Suspending the vagrant box...")
        self.v.suspend()
        out = self.vagrant_status()
	self.assertTrue(out is "paused" or "saved")


    def test_vagrant_resume(self):
    	''' resume the suspended box '''
        self.log.info("Resuming the vagrant box...")
        self.v.resume()
        out = self.vagrant_status()
	self.assertEqual("running", out)


    def test_vagrant_halt(self):
    	''' halt a running vagrant box '''
        self.log.info("Halting the vagrant box...")
        self.v.halt()
        out = self.vagrant_status()
        self.assertTrue(out is "shutoff" or "poweroff")


    def test_vagrant_reload(self):
    	''' reload the halted box '''
        self.log.info("Reloading the vagrant box...")
        self.v.reload()
	out = self.vagrant_status()
        self.assertEqual("running", out)


    def test_vagrant_destroy(self):
    	''' destroy the vagrant box '''
        self.log.info("Destroying the vagrant box...")
        self.v.destroy()
        out = self.vagrant_status()
        self.assertEqual("not_created", out)

