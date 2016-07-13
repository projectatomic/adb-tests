'''
Created on Jun 29, 2016

@author: amit
'''
from avocado.utils import process
import imp
import logging
import time

log = logging.getLogger("Openshift.Debug")

def openshiftLibInfo(self):
    '''
    TBD
    '''
    openshiftUtils = imp.load_source('openshiftUtils', self.params.get('openshift_util_MODULE'))
    self.log.info("Openshift library version : " +openshiftUtils.get_version())
    
def oc_usr_login(self, ip_port, uname, password):
    '''
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc login " +ip_port +" --username=" +uname +" --password=" +password +" --insecure-skip-tls-verify" +"'"
    self.log.info ("Executing : " +strcmd)
    output = process.system_output(strcmd)
    return output

def add_new_project(self, project_name):
    '''
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc new-project " +project_name +"'"
    self.log.info ("Executing : " +strcmd)
    time.sleep(2)
    output = process.system_output(strcmd)
    return output

def add_new_app(self, registry):
    '''
    TBD
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
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc expose service " +service_name +"'"
    time.sleep(10)
    output = process.system_output(strcmd)
    return output

def oc_get_service(self):
    '''
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc get service'"
    output = process.system_output(strcmd)
    return output

def oc_get_pod(self):
    '''
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc get pod'"
    output = process.system_output(strcmd)
    return output

def xip_io(self, service_name, openshift_project_name):
    '''
    TBD
    '''
    strcmd = "curl -I http://" +service_name +"-" +openshift_project_name +".rhel-cdk.10.1.2.2.xip.io/"
    output = process.system_output(strcmd)
    return output

def oc_delete(self, project_name):
    '''
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc delete project " +project_name +"'"
    time.sleep(15)
    output = process.system_output(strcmd)
    return output

def oc_logout(self):
    '''
    TBD
    '''
    strcmd = "vagrant ssh -c 'oc logout'"
    self.log.info ("Executing : " +strcmd)
    #time.sleep(5)
    output = process.system_output(strcmd)
    return output

def new_project(self, url, username, password, projectname, registry, servicename):
    '''
    TBD
    '''
    output = oc_usr_login(self, url, username, password)
    self.assertIn("Login successful", output, "Login failed")
        
    output = add_new_project(self, projectname)
    self.assertIn(projectname, output, "Failed to create " +projectname)
        
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
        
    output = oc_port_expose(self, servicename)
    self.assertIn("exposed", output, "Service failed to expose " +projectname)
                                
    time.sleep(5)
    output = xip_io(self, servicename, projectname)
    self.assertIn("HTTP/1.1 200 OK", output, "curl -I http://" +servicename +"-" +projectname +".rhel-cdk.10.1.2.2.xip.io/ fail to expose to outside")
                                    
    output = oc_get_pod(self)
    self.assertIn("Running", output, "Failed to run pod")
                                        
    output = oc_delete(self, projectname)
    self.assertIn("deleted", output, "Failed to delete " +projectname)
