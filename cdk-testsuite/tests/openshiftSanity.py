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
        preconfiguring the test setup before running each test case
        Arg:
            self (object): Object of the current method
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
        Runs sanity on openshift s2i python source
            1. login
            2. new project create
            3. App deploy using the registry from config file
            4. Validation for successful deployment
            5. Routing
            6. Pod status
            7. project delete
            8. logout
        Args:
            self (object): Object of the current method
            openshift_URL (string) : ip and port of openshift server to be used
            openshift_USERNAME (string): username of openshift web console to be used
            openshift_PASSWORD (string): password of openshift web console to be used
            openshift_python_PROJECT (string): name of the python project to be added to the openshift server
            openshift_python_REGISTRY (string): python registry path/location
            service_python_NAME (string): name of the python service to be exposed outside
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_python_PROJECT'), 
                              self.params.get('openshift_python_REGISTRY'), self.params.get('service_python_NAME'))
    
    def test_ruby_project(self):
        '''
        Runs sanity on openshift s2i ruby source
            1. login
            2. new project create
            3. App deploy using the registry from config file
            4. Validation for successful deployment
            5. Routing
            6. Pod status
            7. project delete
            8. logout
        Args:
            self (object): Object of the current method
            openshift_URL (string) : ip and port of openshift server to be used
            openshift_USERNAME (string): username of openshift web console to be used
            openshift_PASSWORD (string): password of openshift web console to be used
            openshift_ruby_PROJECT (string): name of the ruby project to be added to the openshift server
            openshift_ruby_REGISTRY (string): ruby registry path/location
            service_ruby_NAME (string): name of the ruby service to be exposed outside
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_ruby_PROJECT'), 
                              self.params.get('openshift_ruby_REGISTRY'), self.params.get('service_ruby_NAME'))
    
    def test_perl_project(self):
        '''
        Runs sanity on openshift s2i perl source
            1. login
            2. new project create
            3. App deploy using the registry from config file
            4. Validation for successful deployment
            5. Routing
            6. Pod status
            7. project delete
            8. logout
        Args:
            self (object): Object of the current method
            openshift_URL (string) : ip and port of openshift server to be used
            openshift_USERNAME (string): username of openshift web console to be used
            openshift_PASSWORD (string): password of openshift web console to be used
            openshift_perl_PROJECT (string): name of the perl project to be added to the openshift server
            openshift_perl_REGISTRY (string): perl registry path/location
            service_perl_NAME (string): name of the perl service to be exposed outside
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_perl_PROJECT'), 
                              self.params.get('openshift_perl_REGISTRY'), self.params.get('service_perl_NAME'))
    
    def test_nodejs_project(self):
        '''
        Runs sanity on openshift s2i nodejs source
            1. login
            2. new project create
            3. App deploy using the registry from config file
            4. Validation for successful deployment
            5. Routing
            6. Pod status
            7. project delete
            8. logout
        Args:
            self (object): Object of the current method
            openshift_URL (string) : ip and port of openshift server to be used
            openshift_USERNAME (string): username of openshift web console to be used
            openshift_PASSWORD (string): password of openshift web console to be used
            openshift_nodejs_PROJECT (string): name of the nodejs project to be added to the openshift server
            openshift_nodejs_REGISTRY (string): nodejs registry path/location
            service_nodejs_NAME (string): name of the nodejs service to be exposed outside
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_nodejs_PROJECT'), 
                              self.params.get('openshift_nodejs_REGISTRY'), self.params.get('service_nodejs_NAME'))
    
    def test_php_project(self):
        '''
        Runs sanity on openshift s2i php source
            1. login
            2. new project create
            3. App deploy using the registry from config file
            4. Validation for successful deployment
            5. Routing
            6. Pod status
            7. project delete
            8. logout
        Args:
            self (object): Object of the current method
            openshift_URL (string) : ip and port of openshift server to be used
            openshift_USERNAME (string): username of openshift web console to be used
            openshift_PASSWORD (string): password of openshift web console to be used
            openshift_php_PROJECT (string): name of the php project to be added to the openshift server
            openshift_php_template (string): name of php template
            service_php_NAME (string): name of the php service to be exposed outside
            tepmlate (boolean): True if using template
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_php_PROJECT'), 
                              self.params.get('openshift_php_template'), self.params.get('service_php_NAME'), 
                              tempalte = True)
    
    def test_nodejs_mongodb_template(self):
        '''
        Runs sanity on openshift s2i nodejs with mongodb source
            1. login
            2. new project create
            3. App deploy using the registry from config file
            4. Validation for successful deployment
            5. Routing
            6. Pod status
            7. project delete
            8. logout
        Args:
            self (object): Object of the current method
            openshift_URL (string) : ip and port of openshift server to be used
            openshift_USERNAME (string): username of openshift web console to be used
            openshift_PASSWORD (string): password of openshift web console to be used
            openshift_nodejsmongodb_PROJECT (string): name of the nodejs with mongodb project to be added to the openshift server
            openshift_nodejsmongodb_TEMPLATE (string): name of nodejs with mongodb template
            service_nodejsmongodb_NAME (string): name of the nodejs service to be exposed outside
            tepmlate (boolean): True if using template
            dbservicename (string): Takes name of the database service name 
        '''
        openshift.new_project(self, self.params.get('openshift_URL'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_nodejsmongodb_PROJECT'), 
                              self.params.get('openshift_nodejsmongodb_TEMPLATE'), self.params.get('service_nodejsmongodb_NAME'), 
                              tempalte = True, dbservicename = "mongodb")
    
    def test_logout(self):
        '''
        Loging out the test from openshift server
        Args:
            self (object): Object of the current method
        '''
        output = openshift.oc_logout(self)
        logout_str = "Logged " +"\"" +self.params.get('openshift_USERNAME') +"\"" +" out on " +"\"https://"+self.params.get('openshift_URL') +"\""
        self.assertIn(logout_str, output, "Failed to log out")
