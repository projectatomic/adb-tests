import time
import imp
from avocado import Test
import subprocess
import os
import pexpect
#from Logic import Utils

Utils= imp.load_source('Utils', '../libraries/vagrant/vagrant.py')

class cmd(Test):


    def test_Rhel_hyper_k8_up(self):
        self.log.info("Getting Path to CDK directory")

        path_var = Utils.settingPath(self)
        try:
            globalstatus = Utils.global_status(self, "misc/hyperv/rhel-k8s-singlenode-hyperv")
            self.log.info(
                "Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus.strip())
        except Exception:
            self.log.info("Exception!!")
            globalstatus = 'none'
        finally:

            if (globalstatus.strip() != 'running'):
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus)

                (output, err) = Utils.vagrantUp(self, path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv')
                self.log.debug("Sleep for 40 seconds : Before checking global status")
                globalstatus = Utils.global_status(self, "misc/hyperv/rhel-k8s-singlenode-hyperv")
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus)
                assert globalstatus.strip(), 'running'

            elif (globalstatus.strip() == 'running'):

                globalstatus = Utils.global_status(self, "misc/hyperv/rhel-k8s-singlenode-hyperv")
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus)

    def test_k8_powershell_suspend(self):
        Utils.shell_commands(self,'vagrant status')



    def test_k8_powershell_resume(self):
        Utils.shell_commands(self, 'vagrant resume')

    def test_k8_powershell_halt(self):
        Utils.shell_commands(self, 'vagrant halt')
        psxmlgen = subprocess.Popen([r'C:/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe',
                                     'cd ' + self.params.get(
                                         'vagrant_VARGRANTFILE_DIRS') + 'misc/hyperv/rhel-k8s-singlenode-hyperv | vagrant halt'],
                                    cwd=os.getcwd())
        result = psxmlgen.wait
        time.sleep(20)
        self.log.debug('Resume result :' + str(result))

    def test_k8_powershell_destroy(self):
       Utils.shell_commands(self, 'vagrant destroy --force')






