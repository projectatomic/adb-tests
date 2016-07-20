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
Avocado version 37.0
CDK version 2.1 

How do I Install and Run the openshift sanity test cases ?
1. clone the repository https://github.com/projectatomic/adb-tests/tree/master/cdk-testsuite
2. open the terminal and run the command "avocado run /path_to_test_dir/openshiftSanity.py --multiplex /path_to_config_dir/config.yaml"  

NOTE : Only the input parameters are present in the config file
