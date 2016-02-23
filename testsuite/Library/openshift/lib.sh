#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   lib.sh of /Library/vagrant
#   Description: Library for openshift in vagrant box
#   Author: Ondrej Ptak <optak@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2015 Red Hat, Inc.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   library-prefix = openshift
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 NAME

openshift - Library for openshift in vagrant box

=head1 DESCRIPTION

This is a library for common tasks done with openshift.
Most of the communication with openshift is dome using "vagrant ssh" in vagrant box.

=cut

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 VARIABLES

There are a few input variables you can use to pass settings to this Library,
and also other variables where you can find results of called functions.

=over

=item example

No variables needed (yet).

=back
=cut

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 FUNCTIONS

=head2 openshiftLogin

Login into openshift

Login into openshift (oc login) with username and password provided to this function.
Login to server: localhost:8443, ignoring TLS.

    openshiftLogin username password

Returns 0 when the logging into openshift was successfull, non-zero otherwise.

=cut

openshiftLogin () {
    if [ "$1" == "" -o "$2" == "" ]; then
        rlLogError "openshiftLogin: username and/or password not provided"
        return 1
    fi
    rlRun "vagrant ssh -c 'oc login localhost:8443 -u=$1 -p=$2 --insecure-skip-tls-verify=true'"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 openshiftWait4build

Wait until the build is completed.

    openshiftWait4build build_name timeout

=over

Periodicaly check if build for specified application has been already completed.

=back

Returns 0 when build is successfully built, 1 if build fails or timeout has been reached.

=cut

openshiftWait4build () {
    # openshiftWait4build buildname timeout[min]

    # check validity of buildname
    if [ "$1" == "" ]; then
        rlLogError "openshiftWait4build: no build name provided"
        return 1
    fi

    # check for validity of timeout
    if [ "$2" -le 0 ]; then
        rlLogError "openshiftWait4build: timeout \"\" is not valid"
        return 1
    fi

    # waiting untill build is Completed or timeout
    cnt=0
    while [ $cnt != $2 ]; do
        cnt=$((cnt+1))
        buildstatus=`vagrant ssh -c "oc get builds | grep \"$1\""`
        echo $buildstatus | grep Complete > /dev/null
        if [ $? == 0 ]; then
            vagrant ssh -c "oc get builds | grep \"$1\"" # for more usefull log
            rlLog "Build \"$1\" is Completed"
            return 0
        fi
        echo "$buildstatus"
        sleep 1m
    done

    # timeout
    rlLogError "openshiftWait4build: timeout $2 min reached for build \"$1\""
    vagrant ssh -c "oc get builds" # for more usefull log
    return 1
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 openshiftWait4deploy

Wait until the application is deployed.

    openshiftWait4build build_name timeout

=over

Periodicaly check if application has been already deployed.
Successfull deployment is if all pods are in state running.

=back

Returns 0 when application is deployed, 1 if deployment fails or timeout has been reached.

=cut

openshiftWait4deploy () {
    # openshiftWait4deploy buildname timeout[s]

    # check validity of buildname
    if [ "$1" == "" ]; then
        rlLogError "openshiftWait4build: no build name provided"
        return 1
    fi

    # check for validity of timeout
    if [ "$2" -le 0 ]; then
        rlLogError "openshiftWait4build: timeout \"\" is not valid"
        return 1
    fi

    # waiting untill application is deployed  is Completed or timeout
    cnt=0
    while [ $cnt != $2 ]; do
        cnt=$((cnt+1))
        # TODO: check timeout more precisely, vagrant ssh os long operation
        vagrant ssh -c "oc describe dc/$1 | grep '[0-9]\+ Running / 0 Waiting / 0 Succeeded / 0 Failed'"
        if [ $? == 0 ]; then
            vagrant ssh -c "oc get builds | grep \"$1\"" # for more usefull log
            vagrant ssh -c "oc describe dc/$1"
            pods=`vagrant ssh -c "oc describe dc/$1" | grep 'Pods Status' | awk '{print $3}' | grep -o '[0-9]\+'`
            rlLog "Application \"$1\" is deployed in $pods pod(s)"
            return 0
        fi
        sleep 1
    done

    # timeout
    rlLogError "openshiftWait4build: timeout $2 s reached for deploying application \"$1\""
    vagrant ssh -c "oc get builds" # for more usefull log
    return 1
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# other function

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Verification
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   This is a verification callback which will be called by
#   rlImport after sourcing the library to make sure everything is
#   all right. It makes sense to perform a basic sanity test and
#   check that all required packages are installed. The function
#   should return 0 only when the library is ready to serve.

openshiftLibraryLoaded() {
    # TODO: write something ?
    return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Authors
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 AUTHORS

=over

=item *

Ondrej Ptak <optak@redhat.com>

=back

=cut
