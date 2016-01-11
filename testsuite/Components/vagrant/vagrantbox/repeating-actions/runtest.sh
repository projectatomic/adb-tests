#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of vagrant/vagrantbox/sanity
#   Description: test vagrant-registration plugin with rhel box
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

TEST_COUNT=15 # number of repeating of each subtest

rlJournalStart
    rlPhaseStartSetup
        rlImport 'testsuite/vagrant'
        vagrantBoxIsProvided || rlDie
        vagrantBoxAdd || rlDie
        vagrantConfigureGeneralVagrantfile "skip"
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        pushd $TmpDir
        rlRun "vagrant init $vagrant_BOX_NAME"
        popd
    rlPhaseEnd

  for d in $TmpDir $vagrant_VAGRANTFILE_DIRS; do
        if [ "$d" == "$TmpDir" ]; then
            rlPhaseStartTest "testing new Vagrantfile"
        else
            rlPhaseStartTest "testing Vangrantfile from `basename $d` directory"
        fi
        if ! test -f $d/Vagrantfile ; then
            rlFail "$d/Vagrantfile doesn't exist"
            rlPhaseEnd
            continue
        fi
        rlRun "pushd $d"

        for i in `seq 1 $TEST_COUNT`; do
            rlLogInfo "Testing repeating vagrant up/down: round $i / $TEST_COUNT"
            vagrant up --provider $vagrant_PROVIDER || rlFail "vagrant up failed"
            vagrant ssh -c 'echo hello' | grep hello || rlFail "vagrant ssh failed"
            vagrant halt || rlFail "vagrant halt failed"
        done

        rlRun "vagrant up --provider $vagrant_PROVIDER"
        for i in `seq 1 $TEST_COUNT`; do
            rlLogInfo "Testing repeating vagrant suspend/resume: round $i / $TEST_COUNT"
            vagrant suspend || rlFail "vagrant suspend failed"
            vagrant ssh -c 'echo hello' | grep hello && rlFail "vagrant box shouldn't responde now"
            vagrant resume || rlFail "vagrant resume failed"
            vagrant ssh -c 'echo hello' | grep hello || rlFail "vagrant ssh failed"
        done
        vagrant halt

        for i in `seq 1 $TEST_COUNT`; do
            rlLogInfo "Testing repeating vagrant up/destroy: round $i / $TEST_COUNT"
            vagrant up --provider $vagrant_PROVIDER || rlFail "vagrant up failed"
            vagrant ssh -c 'echo hello' | grep hello || rlFail "vagrant ssh failed"
            vagrant destroy --force || rlFail "vagrant destroy failed"
        done
    rlPhaseEnd

  done

    rlPhaseStartCleanup
        #vagrantBoxRemove # can be shared, so skipping
        rlRun "rm -f ~/.vagrant.d/Vagrantfile"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
