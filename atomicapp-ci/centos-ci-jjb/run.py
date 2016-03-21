#!/usr/bin/python
import json, urllib, subprocess, sys, os

# We will interface with Duffy to request machines:
# Duffy documentation at https://wiki.centos.org/QaWiki/CI/Duffy

# Formulate the url to request nodes
url_base = "http://admin.ci.centos.org:8080"
api_key  = os.environ['CICO_API_KEY'] # comes from node environment vars
count    = os.environ['MACHINE_COUNT']
ver      = "7"
arch     = "x86_64"
req_url  = "%s/Node/get?key=%s&ver=%s&arch=%s&count=%s" % (url_base,api_key,ver,arch,count)

# The git repo url of the project for us to clone
git_repo_url = os.environ['GIT_REPO_URL']
# The test command to run
test_cmd = os.environ['TEST_CMD']

# Make the request - a json string is returned
jsondata = urllib.urlopen(req_url).read()
# load into a dictionary
data = json.loads(jsondata)

# Iterate through the returned hosts and run the tests on it
for host in data['hosts']:
    # Build the ssh part of the cmd to send
    ssh_cmd  = "ssh -t -t " # Force psuedo tty allocation - need two -t
    ssh_cmd += "-o UserKnownHostsFile=/dev/null " # Don't store host info
    ssh_cmd += "-o StrictHostKeyChecking=no "     # Don't ask yes/no
    ssh_cmd += "root@%s " % (host)                # Log in as root on the host

    # Build up cmd to run on the remote duffy instance
    #  - Install git
    #  - Create and change to temporary directory
    #  - Clone remote repo
    #  - Finally run user specified test cmd
    remote_cmd  = 'yum install -y git && '
    remote_cmd += "mkdir /tmp/test && cd /tmp/test && "
    remote_cmd += "git clone %s . && " % git_repo_url
    remote_cmd += '/bin/bash -c ' + test_cmd

    cmd = '%s "%s"' % (ssh_cmd, remote_cmd)
    print("Running cmd: {}".format(cmd))
    exit_code = subprocess.call(cmd, shell=True)

    # Send a rest request to release the node
    done_nodes_url="%s/Node/done?key=%s&ssid=%s" % (url_base, api_key, data['ssid'])
    print urllib.urlopen(done_nodes_url).read()
sys.exit(exit_code)
