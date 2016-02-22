# NAME

openshift - Library for openshift in vagrant box

# DESCRIPTION

This is a library for common tasks done with openshift.
Most of the communication with openshift is dome using "vagrant ssh" in vagrant box.

# VARIABLES

There are a few input variables you can use to pass settings to this Library,
and also other variables where you can find results of called functions.

- example

    No variables needed (yet).

# FUNCTIONS

## openshiftLogin

Login into openshift

Login into openshift (oc login) with username and password provided to this function.
Login to server: localhost:8443, ignoring TLS.

    openshiftLogin username password

Returns 0 when the logging into openshift was successfull, non-zero otherwise.

## openshiftWait4build

Wait until the build is completed.

    openshiftWait4build build_name timeout

> Periodicaly check if build for specified application has been already completed.

Returns 0 when build is successfully built, 1 if build fails or timeout has been reached.

## openshiftWait4deploy

Wait until the application is deployed.

    openshiftWait4build build_name timeout

> Periodicaly check if application has been already deployed.
> Successfull deployment is if all pods are in state running.

Returns 0 when application is deployed, 1 if deployment fails or timeout has been reached.

# AUTHORS

- Ondrej Ptak <optak@redhat.com>
