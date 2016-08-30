#!/usr/bin/python

import os
import subprocess
from avocado.utils import process


def vsm_plugin_install(vagrant_PLUGIN_DIR):
    ''' method installs the cdk vagrant plugins '''
    ''' returns the output of the vagrant plugin install cmd '''
    os.chdir(vagrant_PLUGIN_DIR)
    cmd = "vagrant plugin install ./vagrant-registration-*.gem ./vagrant-sshfs-*.gem ./vagrant-service-manager-*.gem ./landrush-*.gem "
    out = process.run(cmd, shell=True)
    return out


def vsm_env_info(vagrant_BOX_PATH, service, readable):
    ''' method to get the env variable details for 
        services and returns the output of the cmd '''
    os.chdir(vagrant_BOX_PATH)
    cmd = "vagrant service-manager env %s %s" %(service, readable)
    out = process.run(cmd, shell=True)
    return out


def vsm_box_info(vagrant_BOX_PATH, option, readable):
    ''' method to get the box version and ip details 
        and returns the output of the cmd '''
    try:
	os.chdir(vagrant_BOX_PATH)
	cmd = "vagrant service-manager box %s %s" %(option, readable)
    	out = process.run(cmd, shell=True)
    	return out
    except:
	print "Could NOT get the info of the Vagrant box. Maybe something went wrong..."

def vsm_service_handling(vagrant_BOX_PATH, operation, service):
    ''' method to start/stop/restart and get status of 
        services and returns the output of the cmd '''
    os.chdir(vagrant_BOX_PATH)
    cmd = "vagrant service-manager %s %s" %(operation, service)
    out = process.run(cmd, shell=True)
    return out


def vsm_is_service_running(vagrant_BOX_PATH, service):
    ''' checks status of service and returns True if running '''
    try:
        os.chdir(vagrant_BOX_PATH)
        cmd = "vagrant service-manager status %s" %(service)
        out = process.run(cmd, shell=True)
        if "%s - running\n" %(service) == out.stdout:
	    return True
        elif "%s - stopped\n" %(service) == out.stdout:
            return False
    except:
	print "Could NOT get the status of the service. Maybe something went wrong..."

def instll_cli(vagrant_BOX_PATH, service,version,command):
    os.chdir(vagrant_BOX_PATH)
    env_vars = subprocess.Popen('eval "$(VAGRANT_NO_COLOR=1 vagrant service-manager env '+service+' | tr -d \'\r\')";eval "$(vagrant service-manager install-cli '+service+' '+version+' | tr -d \'\r\')";'+command+'',  stdout=subprocess.PIPE, shell=True)
    (output1, err1) = env_vars.communicate()
    return output1,err1

def box_ip(vagrant_BOX_PATH, ip):
    os.chdir(vagrant_BOX_PATH)
    env_vars = subprocess.Popen("vagrant service-manager box %s " %(ip),  stdout=subprocess.PIPE, shell=True)
    (output1, err1) = env_vars.communicate()
    return output1,err1
    





