import time
from avocado import Test
import subprocess
import imp
import vagrant
cdk_utils = imp.load_source('cdk_utils', '/home/naina/PycharmProjects/abcdk/utils/cdk_dependency_util.py')
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
            vagrant_VERSION = vagrant_verification.version()
            self.log.info("Vagrant version is  :: " + vagrant_VERSION)
            self.assertTrue(vagrant_VERSION)








