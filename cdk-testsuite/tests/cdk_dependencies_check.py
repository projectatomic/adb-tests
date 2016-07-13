import time
from avocado import Test
import subprocess
import imp
import vagrant
cdk_utils = imp.load_source('cdk_utils', '../utils/cdk_dependency_util.py')
class cdk_dependencies_check(Test):


    def test_vagrant_verification(self):
        self.log.info("Checking which operating system are you using::")
        machine = cdk_utils.platform_verification(self)
        self.log.info("Verifying Vagrant for :: " +machine)
        vagrant_verification = vagrant.Vagrant()
        try:
            vagrant_VERSION=vagrant_verification.version()
            self.log.info("Vagrant version is  :: " + vagrant_VERSION)
            self.assertTrue(vagrant_VERSION)
        except:
            self.log.info("Vagrant is  not present on Machine ")
            cdk_utils.vagrant_installation(self,machine=machine,sudopassword=self.params.get('SudoPassword'))
            time.sleep(30)
            vagrant_VERSION = vagrant_verification.version()
            self.log.info("Vagrant version is  :: " + vagrant_VERSION)
            self.assertTrue(vagrant_VERSION)

    def test_enable_virtualization_verification(self):
        self.log.info("Testing Enable Virtualization")
        self.log.info("Checking which operating system are you using::")
        machine = cdk_utils.platform_verification(self)
        self.log.info("Verifying Vagrant for :: " +machine)
        vagrant_verification = vagrant.Vagrant()

        try:
            vagrant_installation.enable_virtualization(self,machine=machine,sudopassword=self.params.get('SudoPassword'),sub_username=self.params.get('vagrant_RHN_USERNAME'),sub_password=self.params.get('vagrant_RHN_PASSWORD'))
        except:
            print "anything"







