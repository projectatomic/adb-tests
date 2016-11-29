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
	cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
	self.log.info("Brining up the vagrant box...")
	child = pexpect.spawn (cmd)
	if self.registration_required and not self.credentials_exported:
	    child.expect('.*Would you like to register the system now.*', timeout=300)
	    child.sendline ('n')
	    self.log.info(child.after)
	index = child.expect (['.*assword.*', pexpect.EOF, pexpect.TIMEOUT], timeout=300)
	if index == 0:
	    child.sendline (self.sudo_PASSWORD)
	rc = child.expect(pexpect.EOF, timeout=None)
	self.assertEqual(0, rc, "Vagrant up returned non-zero exit code")
	out = self.vagrant_status()
	self.assertEqual("running", out, "The vagrant box is not running...")
	self.test_vagrant_destroy()

    def test_vagrant_up_register(self):
    	''' vagrant up with registration to RHN '''
	self.test_vagrant_destroy()
        self.log.info("Brining up the vagrant box and registering to RHN...")
        os.environ["SUB_USERNAME"] = self.vagrant_RHN_USERNAME
	os.environ["SUB_PASSWORD"] = self.vagrant_RHN_PASSWORD
	cmd = "vagrant up --provider %s" %(self.vagrant_PROVIDER)
	#child = popen_spawn.PopenSpawn (cmd)
	child = pexpect.spawn (cmd)
	index = child.expect (['.*assword.*', pexpect.EOF, pexpect.TIMEOUT], timeout=300)
	if index == 0:
            child.sendline (self.sudo_PASSWORD)
            self.log.info(child.after)
	rc = child.expect(pexpect.EOF, timeout=None)
	self.assertEqual(0, rc)
	out = self.vagrant_status()
	self.assertEqual("running", out)


    def test_ssh_into_box(self):
    	''' test ssh into the vagrant box '''
	cmd = "vagrant ssh -c 'uname'"
        self.log.info("Checking the ssh access into the vagrant box...")
        out = process.run(cmd, shell=True)
        self.assertEqual("Linux\n", out.stdout)
	self.log.info("ssh access into the vagrant box is successful...")

    def test_vagrant_suspend(self):
    	''' test to suspend the vagrant box '''
        self.log.info("Suspending the vagrant box...")
        self.v.suspend()
        out = self.vagrant_status()
	self.assertTrue(out in self.suspended_state)

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
	self.assertTrue(out in self.halt_state)

    def test_vagrant_reload(self):
    	''' reload the halted box '''
        self.log.info("Reloading the vagrant box...")
        #cmd = "self.v.reload()"
	cmd = "vagrant reload"
	child = pexpect.spawn (cmd)
        index = child.expect (['.*assword.*', pexpect.EOF, pexpect.TIMEOUT], timeout=300)
	if index == 0:
            child.sendline (self.sudo_PASSWORD)
        rc = child.expect(pexpect.EOF, timeout=None)
        self.assertEqual(0, rc)
	out = self.vagrant_status()
        self.assertEqual("running", out)


    def test_vagrant_destroy(self):
    	''' destroy the vagrant box '''
        self.log.info("Destroying the vagrant box...")
        self.v.destroy()
        out = self.vagrant_status()
        self.assertEqual("not_created", out)

