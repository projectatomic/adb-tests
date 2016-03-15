#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of openshift/atomicapp-with-openshift
#   Description: test atomicapp with openshift provider
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

        # check openshift service state
        rlRun "vagrant ssh -c \"systemctl status openshift.service | grep 'active (running)'\"" \
            0 "Service openshift should be running"
      if [ $? == 0 ]; then # test only if openshift is running, otherwise skip

        # oc login, new project, new app, expose
        openshiftLogin openshift-dev devel
        rlRun "vagrant ssh -c 'oc new-project testing'"

        # run container in openshift using atomicapp
        rlRun "vagrant ssh -c 'sudo atomic  run tomaskral/helloflask-atomicapp --provider=openshift --providerconfig=/home/vagrant/.kube/config --namespace=testing'"\
            0 "Running helloflask-atomicapp in openshift"
        rlRun "vagrant ssh -c 'oc expose svc/helloflask-svc'"

        sleep 1m
        rlRun "openshiftWait4deploy rc/helloflask 10" # timeout 10s
        rlRun "openshiftWait4deploy rc/redis-slave 3" # timeout 10s
        rlRun "openshiftWait4deploy rc/redis-master 3" # timeout 10s

        # verification
        rlRun "curl -I helloflask-svc-testing.`vagrantBoxHostname`.10.1.2.2.xip.io | tee header"
        rlAssertGrep "200 OK" header
        rm -f header

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
