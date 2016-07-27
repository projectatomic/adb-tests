What is openshift sanity test cases using oc (openshift cli)?

Sanity test case is the minimum basic test case required to evaluate the product CDK for openshift. Openshift cli is a command line utility for interaction with openshift server. These sanity cases contains 

1. login to openshift server 
2. New project creation
3. Application deployment
4. Routing
5. Pod status
6. project delete
7. logout from openshift server

prerequisites:
Install avocado version 37.0
Install CDK version 2.1 

How do I Install and Run the openshift sanity test cases ?
1. open terminal and create a test directory.
   Example : $ mkdir Test
2. clone the repository https://github.com/projectatomic/adb-tests/tree/master/cdk-testsuite
3. Example : $ cd Test
             $ git clone https://github.com/projectatomic/adb-tests/tree/master/cdk-testsuite
4. Go to the config.yaml file path and update the path and module entries as per the path you cloned.
   Example : $ cd /Test/cdk-testsuite/config
             $ vi config.yaml
             NOTE : Update the path and module entries (path_linux, path_win, path_mac, openshift_lib_MODULE and openshift_util_MODULE)
5. Run the command "avocado run /path_to_test_dir/openshiftSanity.py --multiplex /path_to_config_dir/config.yaml"
   Example : $ avocado run /Test/cdk-testsuite/tests/openshiftSanity.py --multiplex /Test/cdk-testsuite/config/config.yaml
