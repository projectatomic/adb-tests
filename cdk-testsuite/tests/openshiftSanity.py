'''
Created on Jun 29, 2016

@author: amit
'''
from avocado import Test
from avocado import VERSION
import imp
import logging
import os
import platform
import re

log = logging.getLogger("Openshift.Debug")

def new_project(self, port, username, password, projectname, registry, servicename, tempalte = False, dbservicename = "default"):
    '''
    Adding a new application to the project and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        username (string): username of openshift web console to be used
        password (string): password of openshift web console to be used
        projectname (string): name of the project to be added to the openshift server
        registry (string): registry path/location
        servicename (string): name of the service to be exposed outside
        tempalte (boolean): if creating the s2i using openshift template then it takes value as True otherwise the default value False 
        dbservicename (string): Takes the database service name if specified otherwise default
    '''
    output = openshift.oc_usr_login(self, port, username, password)
    self.assertIn("Login successful", output, "Login failed")
        
    output = openshift.add_new_project(self, projectname)
    self.assertIn(projectname, output, "Failed to create " +projectname)
    
    if not tempalte:
        output = openshift.add_new_app(self, registry)
        lst = registry.split("/")
        repo = lst[len(lst) - 1]
        parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %repo, output)
        if parten:
            self.assertIn(parten, output, registry +" deployment failed")
    else:
        output = openshift.add_new_template(self, registry)
        parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %registry, output)
        if parten:
            self.assertIn(parten, output, registry +" deployment failed")
        if "default" not in dbservicename:
            parten = re.search(r"^(?=.*?\bdeploys\b)(?=.*?\b%s\b)(?=.*?\bopenshift/%s\b).*$" %(dbservicename, dbservicename), output)
            if parten:
                self.assertIn(parten, output, dbservicename +" deployment failed")
    if not tempalte:    
        output = openshift.oc_port_expose(self, servicename)
        self.assertIn("exposed", output, "Service failed to expose " +projectname)
    else:
        pass
                                
    output = openshift.routing_cdk(self, servicename, projectname)
    self.assertIn("HTTP/1.1 200 OK", output, "Service " +servicename +"-" +projectname +" fail to expose to outside")
                                    
    output = openshift.oc_get_pod(self)
    self.assertIn("Running", output, "Failed to run pod")
                                        
    output = openshift.oc_delete(self, projectname)
    self.assertIn("deleted", output, "Failed to delete " +projectname)
    
def clean_failed_app(self, projectname):
    output = openshift.oc_delete(self, projectname)
    if output == "FAIL":
        self.log.info("No failed " +projectname +" found")
    else:
        self.log.info("Failed " +projectname +" deleted")
    
class OpenshiftTests(Test):

    def setUp(self):
        '''
        preconfiguring the test setup before running each test case
        Arg:
            self (object): Object of the current method
        '''
        if platform.system() == "Linux":
            os.chdir(self.params.get('path_linux'))
            self.log.info(self.params.get('path_linux'))
        elif platform.system() == "Darwin":
            os.chdir(self.params.get('path_mac'))
            self.log.info(self.params.get('path_mac'))
        else:
            os.chdir(self.params.get('path_win'))
            self.log.info(self.params.get('path_win'))
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
        new_project(self, self.params.get('openshift_WC_PORT'), self.params.get('openshift_USERNAME'), 
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
        clean_failed_app(self, self.params.get('openshift_python_PROJECT'))
        new_project(self, self.params.get('openshift_WC_PORT'), self.params.get('openshift_USERNAME'), 
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
        clean_failed_app(self, self.params.get('openshift_ruby_PROJECT'))
        new_project(self, self.params.get('openshift_WC_PORT'), self.params.get('openshift_USERNAME'), 
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
        clean_failed_app(self, self.params.get('openshift_perl_PROJECT'))
        new_project(self, self.params.get('openshift_WC_PORT'), self.params.get('openshift_USERNAME'), 
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
            tepmlate (boolean): True if using 
        '''
        clean_failed_app(self, self.params.get('openshift_nodejs_PROJECT'))
        new_project(self, self.params.get('openshift_WC_PORT'), self.params.get('openshift_USERNAME'), 
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
            service_php_NAME (string): name of the php service to be exposed outside
            tepmlate (boolean): True if using
            dbservicename (string): Takes name of the database service name 
        '''
        clean_failed_app(self, self.params.get('openshift_php_PROJECT'))
        new_project(self, self.params.get('openshift_WC_PORT'), self.params.get('openshift_USERNAME'), 
                              self.params.get('openshift_PASSWORD'), self.params.get('openshift_nodejsmongodb_PROJECT'), 
                              self.params.get('openshift_nodejsmongodb_TEMPLATE'), self.params.get('service_nodejsmongodb_NAME'), 
                              tempalte = True, dbservicename = "mongodb")
    
    def test_logout(self):
        '''
        Loging out the test from openshift server
        Args:
            self (object): Object of the current method
        '''
        clean_failed_app(self, self.params.get('openshift_nodejsmongodb_PROJECT'))
        output = openshift.oc_logout(self)
        logout_str = "Logged " +"\"" +self.params.get('openshift_USERNAME') +"\"" +" out on " +"\"https://"
        self.assertIn(logout_str, output, "Failed to log out")
