'''
Created on Jun 29, 2016

@author: amit
'''

from avocado.utils import process
import time

version = '1.0'
release = ''

def get_version():
    '''
    Return openshift library version
    '''
    return version +" " + release

def wait_for_output(cmd, timeout = 60):
    output = "FAIL"
    for i in range(timeout):
        time.sleep(1)
        try:
            output = process.system_output(cmd)
            return output
        except:
            pass
    return output

def wait_for_text_in_output(cmd, text = '', timeout = 60):
    output = "FAIL"
    for i in range(timeout):
        time.sleep(1)
        try:
            output = process.system_output(cmd)
            if text in output:
                return output
        except:
            pass
    return output
