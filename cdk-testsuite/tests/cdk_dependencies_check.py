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
            cdk_utils.enable_virtualization(self,machine=machine,sudopassword=self.params.get('SudoPassword'),sub_username=self.params.get('vagrant_RHN_USERNAME'),sub_password=self.params.get('vagrant_RHN_PASSWORD'))
        except:
            print "anything"

    def test_virtualbox(self):
        self.log.info("Verification check for virtual box installation")
        self.log.info("Checking which operating system are you using::")
        machine = cdk_utils.platform_verification(self)
        cdk_utils.virtualbox_installation(self,machine=machine,sudopassword=self.params.get('SudoPassword'))

if __name__ == '__main__':
    print "working"
    #test_vagrant_verification(self)







