import time
from avocado import Test
import imp
Utils = imp.load_source('Utils', '/cygdrive/c/Users/naina/Downloads/ACDK/ACDK/Logic/Utils.py')

class VagrantTests(Test):



    def test(self):
        sleep_length = self.params.get('sleep_length', default=1)
        self.log.debug("Sleeping for %.2f seconds", sleep_length)
        time.sleep(sleep_length)
        path_var=Utils.settingPath(self)
        self.log.debug(str(path_var))


    def Rhel_ose_up(self):
        self.log.info("Getting Path to CDK directory")

        path_var = Utils.settingPath(self)
        try:
            globalstatus = Utils.global_status(self,"rhel-ose")
            self.log.info("Status of " + path_var + 'rhel-ose' + "  " + globalstatus.strip())
        except:
            self.log.info("Exception!!")
            globalstatus='none'
        finally:

            if(globalstatus.strip() !='running'):
                self.log.info("Status of " + path_var + 'rhel-ose' + "  " + globalstatus)

                (output, err) = Utils.vagrantUp(self, path_var + 'rhel-ose')
                self.log.debug(output)
                self.log.debug(err)
                time.sleep(40)
                self.log.debug("Sleep for 40 seconds : Before checking global status")
                globalstatus = Utils.global_status(self, "rhel-ose")
                self.log.info("Status of " + path_var + 'rhel-ose' + "  " + globalstatus)
                assert globalstatus.strip(),'running'

            elif(globalstatus.strip() =='running'):

                globalstatus=Utils.global_status(self, "rhel-ose")
                self.log.info("Status of "+path_var + 'rhel-ose'+"  "+globalstatus)

    def test_Rhel_k8_up(self):
        self.log.info("Getting Path to CDK directory")

        path_var = Utils.settingPath(self)
        try:
            globalstatus = Utils.global_status(self, "misc/rhel-k8s-singlenode-setup")
            self.log.info("Status of " + path_var + 'misc/rhel-k8s-singlenode-setup' + "  " + globalstatus.strip())
        except Exception:
            self.log.info("Exception!!")
            globalstatus = 'none'
        finally:

            if (globalstatus.strip() != 'running'):
                self.log.info("Status of " + path_var + 'misc/rhel-k8s-singlenode-setup' + "  " + globalstatus)

                (output, err) = Utils.vagrantUp(self, path_var + 'misc/rhel-k8s-singlenode-setup')
                #self.log.debug(output)
                #self.log.debug(err)
                time.sleep(40)
                self.log.debug("Sleep for 40 seconds : Before checking global status")
                globalstatus = Utils.global_status(self, "misc/rhel-k8s-singlenode-setup")
                self.log.info("Status of " + path_var + 'misc/rhel-k8s-singlenode-setup' + "  " + globalstatus)
                assert globalstatus.strip(), 'running'

            elif (globalstatus.strip() == 'running'):

                globalstatus = Utils.global_status(self, "misc/rhel-k8s-singlenode-setup")
                self.log.info("Status of " + path_var + 'misc/rhel-k8s-singlenode-setup' + "  " + globalstatus)

    def test_Rhel_ose_hyperv_up(self):
        self.log.info("Getting Path to CDK directory")

        path_var = Utils.settingPath(self)
        try:
            globalstatus = Utils.global_status(self, "misc/rhel-k8s-singlenode-setup")
            self.log.info("Status of " + path_var + 'misc/rhel-k8s-singlenode-setup' + "  " + globalstatus.strip())
        except Exception:
            self.log.info("Exception!!")
            globalstatus = 'none'
        finally:

            if (globalstatus.strip() != 'running'):
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-ose-hyperv' + "  " + globalstatus)

                (output, err) = Utils.vagrantUp(self, path_var + 'misc/hyperv/rhel-ose-hyperv')
                # self.log.debug(output)
                # self.log.debug(err)
                time.sleep(40)
                self.log.debug("Sleep for 40 seconds : Before checking global status")
                globalstatus = Utils.global_status(self, "misc/hyperv/rhel-ose-hypervp")
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-ose-hyperv' + "  " + globalstatus)
                assert globalstatus.strip(), 'running'

            elif (globalstatus.strip() == 'running'):

                globalstatus = Utils.global_status(self, "misc/hyperv/rhel-ose-hyperv")
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-ose-hyperv' + "  " + globalstatus)

    def test_Rhel_hyper_k8_up(self):
        self.log.info("Getting Path to CDK directory")

        path_var = Utils.settingPath(self)
        try:
            globalstatus = Utils.global_status(self, "misc/hyperv/rhel-k8s-singlenode-hyperv")
            self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus.strip())
        except Exception:
            self.log.info("Exception!!")
            globalstatus = 'none'
        finally:

            if (globalstatus.strip() != 'running'):
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus)

                (output, err) = Utils.vagrantUp(self, path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv')
                # self.log.debug(output)
                # self.log.debug(err)
                time.sleep(40)
                self.log.debug("Sleep for 40 seconds : Before checking global status")
                globalstatus = Utils.global_status(self, "misc/hyperv/rhel-k8s-singlenode-hyperv")
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus)
                assert globalstatus.strip(), 'running'

            elif (globalstatus.strip() == 'running'):

                globalstatus = Utils.global_status(self, "misc/hyperv/rhel-k8s-singlenode-hyperv")
                self.log.info("Status of " + path_var + 'misc/hyperv/rhel-k8s-singlenode-hyperv' + "  " + globalstatus)

