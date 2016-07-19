'''
Created on Jun 29, 2016

@author: amit
'''
from avocado.utils import process
import imp
import logging
import re
import time

log = logging.getLogger("Openshift.Debug")


def openshiftLibInfo(self):
    '''
    Get openshift user defined library version
    Args:
        self (object): Object of the current method
    '''
    openshiftUtils = imp.load_source('openshiftUtils', self.params.get('openshift_util_MODULE'))
    self.log.info("Openshift library version : " +openshiftUtils.get_version())
    
def oc_usr_login(self, ip_port, uname, password):
    '''
    Login to openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        ip_port (str): ip and port of openshift to be used
        uname (str): username of openshift web console to be used
        password (str): password of openshift web console to be used
    '''
    strcmd = "vagrant ssh -c 'oc login " +ip_port +" --username=" +uname +" --password=" +password +" --insecure-skip-tls-verify" +"'"
    self.log.info ("Executing : " +strcmd)
    output = process.system_output(strcmd)
    return output

def add_new_project(self, project_name):
    '''
    Adding new project to openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        project_name (str): name of the project to be added to the openshift server
    '''
    strcmd = "vagrant ssh -c 'oc new-project " +project_name +"'"
    self.log.info ("Executing : " +strcmd)
    time.sleep(2)
    output = process.system_output(strcmd)
    return output

def add_new_app(self, registry):
    '''
    Adding new application to new project created for openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        registry (str): registry path/location
    '''
    strcmd = "vagrant ssh -c 'oc new-app " +registry +"'"
    lst = registry.split("/")
    repo = lst[len(lst) - 1]
    self.log.info ("Executing : " +strcmd)
    time.sleep(2)
                
    lst = []
    output = process.system_output(strcmd)
    for lines in output.splitlines():
        if repo in lines:
            lst.append(lines)
                
    lst = lst[len(lst) - 1].split("'") 
    strcmd1 = "vagrant ssh -c " +"'" +lst[1] +"'"
    self.log.info ("Executing : " +strcmd1) 
    time.sleep(30)
                       
        
    output = process.system_output(strcmd1)
    strcmd2 = "vagrant ssh -c 'oc status -v'"
    self.log.info ("Executing : " +strcmd2)
    time.sleep(2)

    output = process.system_output(strcmd2)
    return output

def oc_port_expose(self, service_name):
    '''
    Service port to expose outside and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        service_name (str): name of the service to be exposed outside
    '''
    strcmd = "vagrant ssh -c 'oc expose service " +service_name +"'"
    time.sleep(10)
    output = process.system_output(strcmd)
    return output

def oc_get_service(self):
    '''
    Get the service name of the application and returns output of the oc command executed
    Args:
        self (object): Object of the current method
    '''
    strcmd = "vagrant ssh -c 'oc get service'"
    output = process.system_output(strcmd)
    return output

def oc_get_pod(self):
    '''
    Get the pods details of the containerized application and returns output of the oc command executed
    Args:
        self (object): Object of the current method
    '''
    strcmd = "vagrant ssh -c 'oc get pod'"
    output = process.system_output(strcmd)
    return output

def xip_io(self, service_name, openshift_project_name):
    '''
    check xip.io runs a custom DNS server on the public Internet and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        service_name (string): name of the service to be exposed outside
        openshift_project_name (string): name of the project to be added to the openshift server
    '''
    strcmd = "curl -I http://" +service_name +"-" +openshift_project_name +".rhel-cdk.10.1.2.2.xip.io/"
    output = process.system_output(strcmd)
    return output

def oc_delete(self, project_name):
    '''
    Delete the openshift project and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        openshift_project_name (string): name of the project to be added to the openshift server
    '''
    strcmd = "vagrant ssh -c 'oc delete project " +project_name +"'"
    time.sleep(15)
    output = process.system_output(strcmd)
    return output

def oc_logout(self):
    '''
    logout from openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
    '''
    strcmd = "vagrant ssh -c 'oc logout'"
    self.log.info ("Executing : " +strcmd)
    output = process.system_output(strcmd)
    return output

def add_new_template(self, template):
    '''
    Adding new template to openshift server and returns output of the oc command executed
    Args:
        self (object): Object of the current method
        template (string): name of the openshift template
    '''
    strcmd = "vagrant ssh -c 'oc new-app --template=" +template +"'"
    self.log.info ("Executing : " +strcmd)
        
    lst = []
    output = process.system_output(strcmd)
    for lines in output.splitlines():
        if template in lines:
            lst.append(lines)
                
    lst = lst[len(lst) - 1].split("'") 
    strcmd1 = "vagrant ssh -c " +"'" +lst[1] +"'"
    self.log.info ("Executing : " +strcmd1) 
    time.sleep(30)
    output = process.system_output(strcmd1)
    
    strcmd2 = "vagrant ssh -c 'oc status -v'"
    self.log.info ("Executing : " +strcmd2)
    time.sleep(2)
    output = process.system_output(strcmd2)
    
    return output

def new_project(self, url, username, password, projectname, registry, servicename, tempalte = False, dbservicename = "default"):
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
    output = oc_usr_login(self, url, username, password)
    self.assertIn("Login successful", output, "Login failed")
        
    output = add_new_project(self, projectname)
    self.assertIn(projectname, output, "Failed to create " +projectname)
    
    if not tempalte:
        output = add_new_app(self, registry)
        partenLst = []
        lst = registry.split("/")
        repo = lst[len(lst) - 1]
        for lines in output.splitlines():
            parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %repo, lines)
            partenLst.append(parten)
        match = "NotFound"
        for i in partenLst:
            if i != None:
                match = "Found"
                break
        self.assertIn("NotFound", match, registry +" deployment failed")
    else:
        output = add_new_template(self, registry)
        partenLst = []
        for lines in output.splitlines():
            parten = re.search(r"^(?=.*?\b\\*\b)(?=.*?\bfailed\b)(?=.*?\b%s\b).*$" %registry, lines)
            partenLst.append(parten)
        match = "NotFound"
        for i in partenLst:
            if i != None:
                match = "Found"
                break
        self.assertIn("NotFound", match, registry +" deployment failed")
        if "default" not in dbservicename:
            del partenLst[:]
            for lines in output.splitlines():
                parten = re.search(r"^(?=.*?\bdeploys\b)(?=.*?\b%s\b)(?=.*?\bopenshift/%s\b).*$" %(dbservicename, dbservicename), lines)
                partenLst.append(parten)
            match = "NotFound"
            for i in partenLst:
                if i != None:
                    match = "Found"
                    break
            self.assertIn("Found", match, dbservicename +" deployment failed")
            
    if not tempalte:    
        output = oc_port_expose(self, servicename)
        self.assertIn("exposed", output, "Service failed to expose " +projectname)
    else:
        pass
                                
    time.sleep(60)
    output = xip_io(self, servicename, projectname)
    self.assertIn("HTTP/1.1 200 OK", output, "curl -I http://" +servicename +"-" +projectname +".rhel-cdk.10.1.2.2.xip.io/ fail to expose to outside")
                                    
    output = oc_get_pod(self)
    self.assertIn("Running", output, "Failed to run pod")
                                        
    output = oc_delete(self, projectname)
    self.assertIn("deleted", output, "Failed to delete " +projectname)
