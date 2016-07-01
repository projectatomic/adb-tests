import time
import imp
from avocado import Test
import subprocess
import os
import pexpect
#from Logic import vagrant_lib

vagrant_lib= imp.load_source('vagrant_lib', '/cygdrive/c/Users/naina/Downloads/ACDK/ACDK/Logic/Utils.py')

class cmd(Test):


    
                
    
    def test_vagrant_up(self):
        self.log.info("Getting Path to CDK directory")
        vagrnat_up_dirs=self.params.get('vagrant_UP_FILES')
        self.log.info('These are the locations of Vagrant files ::')
        
        for x in vagrnat_up_dirs.split(',') :
            self.log.info(x)
            path_var = self.params.get('vagrant_VARGRANTFILE_DIRS')
            try:
                (output, err) = vagrant_lib.vagrantUp(self, path_var + x)
                self.log.debug("Sleep for 40 seconds : Before checking global status")
                globalstatus = vagrant_lib.global_status(self, path_var+x)
                self.log.info("Status of 1" + path_var + x + "  " + globalstatus+"***")
                assert globalstatus, 'running'
               
            except Exception:
                self.log.info("Exception!!")
                
            finally:
                globalstatus = vagrant_lib.global_status(self,path_var+ x)
                self.log.info("Status of 2" + path_var + x + "  " + str( globalstatus )+"***")
                if  'running' in globalstatus :
                    self.log.info("Status of " + path_var + x + "  " +str( globalstatus)+"***")
                    (output, err) = vagrant_lib.vagrantUp(self, path_var + x)
                    self.log.debug("Sleep for 40 seconds : Before checking global status")
                    time.sleep(40)
                    globalstatus = vagrant_lib.global_status(self, path_var+x)
                    self.log.info("Status of 3" + path_var + x + "  " + str(globalstatus))
                    assert globalstatus, 'running'

                    

                elif 'running' not in globalstatus :

                    globalstatus = vagrant_lib.global_status(self,path_var+ x)
                    self.log.info("Status of " + path_var + x + "  " + str(globalstatus))



    def test_k8_powershell_status(self):
        if self.params.get('Windows_Shell') == 'powershell':
            operator = '|'
        elif self.params.get('Windows_Shell') == 'cmd':
            operator = '&'
        else:
            operator='&&'
        vagrnat_up_dirs=self.params.get('vagrant_UP_FILES')
        self.log.info('These are the locations of Vagrant files ::')
        
        for x in vagrnat_up_dirs.split(',') :

            output=vagrant_lib.shell_commands(self,'cd ' + self.params.get('vagrant_VARGRANTFILE_DIRS') + x+' ' + operator + ' vagrant status' )
            self.assertTrue('running' in output)
        



    def test_k8_powershell_resume(self):
        if self.params.get('Windows_Shell') == 'powershell':
            operator = '|'
        elif self.params.get('Windows_Shell') == 'cmd':
            operator = '&'
        else:
            operator='&&'
        vagrnat_up_dirs=self.params.get('vagrant_UP_FILES')
        self.log.info('These are the locations of Vagrant files ::')
        
        for x in vagrnat_up_dirs.split(',') :
            output=vagrant_lib.shell_commands(self, 'cd ' + self.params.get('vagrant_VARGRANTFILE_DIRS') + x+' ' + operator + 'vagrant resume')
            self.assertTrue('Resuming' in output)
    

    def test_k8_powershell_destroy(self):
        if self.params.get('Windows_Shell') == 'powershell':
            operator = '|'
        elif self.params.get('Windows_Shell') == 'cmd':
            operator = '&'
        else:
            operator='&&'
        vagrnat_up_dirs=self.params.get('vagrant_UP_FILES')
        self.log.info('These are the locations of Vagrant files ::')
        
        for x in vagrnat_up_dirs.split(',') :
            output=vagrant_lib.shell_commands(self,  'cd ' + self.params.get('vagrant_VARGRANTFILE_DIRS') + x+' ' + operator + 'vagrant destroy --force')
            self.assertTrue('Deleting' in output)  






