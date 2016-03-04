#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of openshift/sanity
#   Description: test basic openshift functionality
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

# Include Beaker environment
. /usr/share/beakerlib/beakerlib.sh || exit 1

rlJournalStart
    rlPhaseStartSetup
        rlImport 'testsuite/vagrant' || rlDie
        rlImport 'testsuite/openshift' || rlDie
        vagrantBoxIsProvided || rlDie
        vagrantBoxAdd || rlDie
        vagrantPluginInstall vagrant-service-manager
        vagrantConfigureGeneralVagrantfile skip
        # check if Vagrntfile for openshift was provided
        rhel_ose_found=false
        for dir in $vagrant_VAGRANTFILE_DIRS; do
            echo $dir | grep "rhel-ose/\?$"
            if [ $? == 0 ]; then
                test -f $dir/Vagrantfile || rlDie "Vagrantfile for openshift not found"
                rlRun "pushd $dir"
                rhel_ose_found=true
                break
            fi
        done
        if [ "$rhel_ose_found" == false ]; then
            rlDie "Vagrantfile for openshift not found"
        fi
    rlPhaseEnd

    rlPhaseStartTest
        # run VM
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello" 0 "ssh to box works"

        # get openshift url

        # check openshift status
        #rlRun "vagrant ssh -c 'oc status'"
        #bash

        # check openshift service state
        rlRun "vagrant ssh -c 'systemctl status openshift.service | grep enabled'" \
            0 "Service openshift should be enabled"
        rlRun "vagrant ssh -c 'systemctl status openshift.service | grep \\\"active (running)\\\"'" \
            0 "Service openshift should be running"
      if [ $? == 0 ]; then # test only if openshift is running, otherwise skip

        # oc login, new project, new app, expose
        openshiftLogin openshift-dev devel
        rlRun "vagrant ssh -c 'oc new-project test_ruby'"
        rlRun "vagrant ssh -c 'oc new-app openshift/ruby-20-centos7~https://github.com/openshift/ruby-hello-world.git'"
        rlRun "openshiftWait4build ruby-hello-world 7"   # timeout 5m
        rlRun "openshiftWait4deploy ruby-hello-world 10" # timeout 10s
        rlRun "vagrant ssh -c 'oc expose service/ruby-hello-world --hostname rhw.10.1.2.2.xip.io'"
        sleep 5

        # check service outside of the box
        rlRun "curl -I http://rhw.10.1.2.2.xip.io/ | tee header | grep '200 OK'"\
            0 "Application is accessible on http://rhw.10.1.2.2.xip.io/"
        cat header; rm -f header
        rlRun "curl -I http://www.10.1.2.2.xip.io/ | tee header | grep '200 OK'"\
            1 "Application is not accessible on http://www.10.1.2.2.xip.io/"
        cat header; rm -f header
        rlRun "curl -I http://rhw.10.1.2.2.xip.io/ | tee header | grep '200 OK'"\
            0 "Application is accessible on http://rhw.10.1.2.2.xip.io/"
        cat header; rm -f header

        # TODO: enhance this test, some ideas below
        # oc status & other info

        # scale

        # systemctl stop,status,start,status,restart,status openshift.service
        # test openshift
        # vagrant halt|up
        # test openshift

        #rlRun "vagrant service-manager env docker > stdout 2> stderr"
        #echo -e "stdout:\n========"
        #cat stdout
        #echo -e "stderr:\n========"
        #cat stderr
        #echo "========"
        #rlAssertNotGrep "." stderr
        #rlAssertGrep "DOCKER_HOST=tcp://[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*:[0-9]*" stdout
      fi
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "vagrant destroy -f"
        rlRun "popd"
        #vagrantBoxRemove # can be shared, so skipping
        rlRun "rm -f ~/.vagrant.d/Vagrantfile"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
