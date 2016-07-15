'''
Created on Jun 29, 2016

@author: amit
'''
from avocado import Test
from avocado import VERSION
import imp
import logging
import os

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
        self.log.info("###########################################################################################")
        self.log.info(openshift.openshiftLibInfo(self))
        self.log.info("Avocado version : %s" % VERSION)
        self.log.info("###########################################################################################")
           
    def test_python_project(self):
        '''
        TBD
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_python_PROJECT'), 
                              self.params.get('openshift_python_REGISTRY'), self.params.get('service_python_NAME'))
    
    def test_ruby_project(self):
        '''
        TBD
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_ruby_PROJECT'), 
                              self.params.get('openshift_ruby_REGISTRY'), self.params.get('service_ruby_NAME'))
    
    def test_perl_project(self):
        '''
        TBD
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_perl_PROJECT'), 
                              self.params.get('openshift_perl_REGISTRY'), self.params.get('service_perl_NAME'))
    
    def test_nodejs_project(self):
        '''
        TBD
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_nodejs_PROJECT'), 
                              self.params.get('openshift_nodejs_REGISTRY'), self.params.get('service_nodejs_NAME'))
    
    def test_php_project(self):
        '''
        TBD
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_php_PROJECT'), 
                              self.params.get('openshift_php_template'), self.params.get('service_php_NAME'), 
                              tempalte = True)
    
    def test_nodejs_mongodb_template(self):
        '''
        TBD
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_nodejsmongodb_PROJECT'), 
                              self.params.get('openshift_nodejsmongodb_TEMPLATE'), self.params.get('service_nodejsmongodb_NAME'), 
                              tempalte = True, dbservicename = "mongodb")
    
    def test_logout(self):
        '''
        TBD
        '''
        output = openshift.oc_logout(self)
        logout_str = "Logged " +"\"" +self.params.get('openshift_USERNAME') +"\"" +" out on " +"\"https://"+self.params.get('openshift_URL') +"\""
        self.assertIn(logout_str, output, "Failed to log out")
