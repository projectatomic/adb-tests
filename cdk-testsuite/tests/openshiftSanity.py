'''
Created on Jun 29, 2016

@author: amit
'''
import time
from avocado import Test
import logging
import os
import imp
import re

log = logging.getLogger("Openshift.Debug")

class OpenshiftTests(Test):

    def setUp(self):
        '''
        TBD
        '''
        if os.name == "posix":
            os.chdir(self.params.get('path_linux'))
            self.log.info(self.params.get('path_linux'))
        elif os.name == "nt":
            os.chdir(self.params.get('path_win'))
            self.log.info(self.params.get('path_win'))
        else:
            os.chdir(self.params.get('path_mac'))
            self.log.info(self.params.get('path_mac'))
        global openshift
        openshift = imp.load_source('openshift', self.params.get('openshift_lib_MODULE'))
        
    def test_oc_new_python_project(self):
        '''
        TBD
        '''
        output = openshift.oc_usr_login(self, self.params.get('openshift_console_URL'), self.params.get('openshift_login_USERNAME'), self.params.get('openshift_login_PASSWORD'))
        self.log.info(output)
        self.assertIn("Login successful", output, "Login failed")
        
        output = openshift.add_new_project(self, self.params.get('openshift_new_python_PROJECT'))
        self.assertIn(self.params.get('openshift_new_python_PROJECT'), output, "Failed to create " +self.params.get('openshift_new_python_PROJECT'))
        
        output = openshift.add_new_app(self, self.params.get('openshift_python_REGISTRY'))
        partenLst = []
        lst = self.params.get('openshift_python_REGISTRY').split("/")
        repo = lst[len(lst) - 1]
        for lines in output.splitlines():
            parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %repo, lines)
            partenLst.append(parten)
        match = "NotFound"
        for i in partenLst:
            if i != None:
                match = "Found"
                break
        self.assertIn("NotFound", match, self.params.get('openshift_python_REGISTRY') +" deployment failed")
        
        output = openshift.oc_port_expose(self, self.params.get('service_python_NAME'))
        self.assertIn("exposed", output, "Service failed to expose " +self.params.get('openshift_new_python_PROJECT'))
                                
        time.sleep(5)
        output = openshift.xip_io(self, self.params.get('service_python_NAME'), self.params.get('openshift_new_python_PROJECT'))
        self.assertIn("HTTP/1.1 200 OK", output, "curl -I http://" +self.params.get('service_python_NAME') +"-" +self.params.get('openshift_new_python_PROJECT') +".rhel-cdk.10.1.2.2.xip.io/ fail to expose to outside")
                                    
        output = openshift.oc_get_pod(self)
        self.assertIn("Running", output, "Failed to run pod")
                                        
        output = openshift.oc_delete(self, self.params.get('openshift_new_python_PROJECT'))
        self.assertIn("deleted", output, "Failed to delete " +self.params.get('openshift_new_python_PROJECT'))
                                        
    def test_oc_new_ruby_project(self):
        '''
        TBD
        '''
        output = openshift.oc_usr_login(self, self.params.get('openshift_console_URL'), self.params.get('openshift_login_USERNAME'), self.params.get('openshift_login_PASSWORD'))
        self.log.info(output)
        self.assertIn("Login successful", output, "Login failed")
        
        output = openshift.add_new_project(self, self.params.get('openshift_new_ruby_PROJECT'))
        self.assertIn(self.params.get('openshift_new_ruby_PROJECT'), output, "Failed to create " +self.params.get('openshift_new_ruby_PROJECT'))
        
        output = openshift.add_new_app(self, self.params.get('openshift_ruby_REGISTRY'))
        partenLst = []
        lst = self.params.get('openshift_ruby_REGISTRY').split("/")
        repo = lst[len(lst) - 1]
        for lines in output.splitlines():
            parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %repo, lines)
            partenLst.append(parten)
        match = "NotFound"
        for i in partenLst:
            if i != None:
                match = "Found"
                break
        self.assertIn("NotFound", match, self.params.get('openshift_ruby_REGISTRY') +" deployment failed")
        
        output = openshift.oc_port_expose(self, self.params.get('service_ruby_NAME'))
        self.assertIn("exposed", output, "Service failed to expose " +self.params.get('openshift_new_python_PROJECT'))
                                
        time.sleep(5)
        output = openshift.xip_io(self, self.params.get('service_ruby_NAME'), self.params.get('openshift_new_ruby_PROJECT'))
        self.assertIn("HTTP/1.1 200 OK", output, "curl -I http://" +self.params.get('service_ruby_NAME') +"-" +self.params.get('openshift_new_ruby_PROJECT') +".rhel-cdk.10.1.2.2.xip.io/ fail to expose to outside")
                                    
        output = openshift.oc_get_pod(self)
        self.assertIn("Running", output, "Failed to run pod")
                                        
        output = openshift.oc_delete(self, self.params.get('openshift_new_ruby_PROJECT'))
        self.assertIn("deleted", output, "Failed to delete " +self.params.get('openshift_new_ruby_PROJECT'))
    
    def test_oc_new_perl_project(self):
        '''
        TBD
        '''
        output = openshift.oc_usr_login(self, self.params.get('openshift_console_URL'), self.params.get('openshift_login_USERNAME'), self.params.get('openshift_login_PASSWORD'))
        self.log.info(output)
        self.assertIn("Login successful", output, "Login failed")
        
        output = openshift.add_new_project(self, self.params.get('openshift_new_perl_PROJECT'))
        self.assertIn(self.params.get('openshift_new_perl_PROJECT'), output, "Failed to create " +self.params.get('openshift_new_perl_PROJECT'))
        
        output = openshift.add_new_app(self, self.params.get('openshift_perl_REGISTRY'))
        partenLst = []
        lst = self.params.get('openshift_perl_REGISTRY').split("/")
        repo = lst[len(lst) - 1]
        for lines in output.splitlines():
            parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %repo, lines)
            partenLst.append(parten)
        match = "NotFound"
        for i in partenLst:
            if i != None:
                match = "Found"
                break
        self.assertIn("NotFound", match, self.params.get('openshift_perl_REGISTRY') +" deployment failed")
        
        output = openshift.oc_port_expose(self, self.params.get('service_perl_NAME'))
        self.assertIn("exposed", output, "Service failed to expose " +self.params.get('openshift_new_perl_PROJECT'))
                                
        time.sleep(5)
        output = openshift.xip_io(self, self.params.get('service_perl_NAME'), self.params.get('openshift_new_perl_PROJECT'))
        self.assertIn("HTTP/1.1 200 OK", output, "curl -I http://" +self.params.get('service_perl_NAME') +"-" +self.params.get('openshift_new_perl_PROJECT') +".rhel-cdk.10.1.2.2.xip.io/ fail to expose to outside")
                                    
        output = openshift.oc_get_pod(self)
        self.assertIn("Running", output, "Failed to run pod")
                                        
        output = openshift.oc_delete(self, self.params.get('openshift_new_perl_PROJECT'))
        self.assertIn("deleted", output, "Failed to delete " +self.params.get('openshift_new_perl_PROJECT'))
    
    def test_oc_new_nodejs_project(self):
        '''
        TBD
        '''
        output = openshift.oc_usr_login(self, self.params.get('openshift_console_URL'), self.params.get('openshift_login_USERNAME'), self.params.get('openshift_login_PASSWORD'))
        self.log.info(output)
        self.assertIn("Login successful", output, "Login failed")
        
        output = openshift.add_new_project(self, self.params.get('openshift_new_nodejs_PROJECT'))
        self.assertIn(self.params.get('openshift_new_nodejs_PROJECT'), output, "Failed to create " +self.params.get('openshift_new_nodejs_PROJECT'))
        
        output = openshift.add_new_app(self, self.params.get('openshift_nodejs_REGISTRY'))
        partenLst = []
        lst = self.params.get('openshift_nodejs_REGISTRY').split("/")
        repo = lst[len(lst) - 1]
        for lines in output.splitlines():
            parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %repo, lines)
            partenLst.append(parten)
        match = "NotFound"
        for i in partenLst:
            if i != None:
                match = "Found"
                break
        self.assertIn("NotFound", match, self.params.get('openshift_nodejs_REGISTRY') +" deployment failed")
        
        output = openshift.oc_port_expose(self, self.params.get('service_nodejs_NAME'))
        self.assertIn("exposed", output, "Service failed to expose " +self.params.get('openshift_new_nodejs_PROJECT'))
                                
        time.sleep(5)
        output = openshift.xip_io(self, self.params.get('service_nodejs_NAME'), self.params.get('openshift_new_nodejs_PROJECT'))
        self.assertIn("HTTP/1.1 200 OK", output, "curl -I http://" +self.params.get('service_nodejs_NAME') +"-" +self.params.get('openshift_new_nodejs_PROJECT') +".rhel-cdk.10.1.2.2.xip.io/ fail to expose to outside")
                                    
        output = openshift.oc_get_pod(self)
        self.assertIn("Running", output, "Failed to run pod")
                                        
        output = openshift.oc_delete(self, self.params.get('openshift_new_nodejs_PROJECT'))
        self.assertIn("deleted", output, "Failed to delete " +self.params.get('openshift_new_nodejs_PROJECT'))
    
    def test_oc_logout(self):
        '''
        TBD
        '''
        output = openshift.oc_logout(self)
        logout_str = "Logged " +"\"" +self.params.get('openshift_login_USERNAME') +"\"" +" out on " +"\"https://"+self.params.get('openshift_console_URL') +"\""
        self.assertIn(logout_str, output, "Failed to log out")


            
