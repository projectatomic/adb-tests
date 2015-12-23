#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of vagrant/adbinfo-plugin/smoke
#   Description: Simple smoke test of adbinfo plugin
#   Author: David Kutalek <dkutalek@redhat.com>
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
        rlImport 'testsuite/vagrant'
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"
        vagrantPluginInstall vagrant-adbinfo
        vagrantConfigureGeneralVagrantfile "skip"
    rlPhaseEnd

    rlPhaseStartTest without_running_vm
        vagrant adbinfo
        rlRun "vagrant adbinfo 2>&1 | grep 'target machine is required to run'"
    rlPhaseEnd

    rlPhaseStartTest with_running_vm
        rlRun "vagrant init $vagrant_BOX_NAME"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant adbinfo > output 2> errors"
        echo -e "stdout:\n========"
        cat output
        echo -e "stderr:\n========"
        cat errors
        echo "========"
        # check output
        rlRun "grep '.' errors" 1 "There should be nothing on stderr"
        rlAssertGrep "DOCKER_HOST=tcp://[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*:[0-9]*" output
        rlAssertGrep "DOCKER_CERT_PATH=.*.docker" output
        rlAssertGrep "DOCKER_TLS_VERIFY=1" output
        rlAssertGrep "DOCKER_MACHINE_NAME=[0-9a-f]*" output
        rlAssertGrep 'eval "$(vagrant adbinfo)' output
        rlAssertNotGrep 'error\|fail' output -i
    rlPhaseEnd


    rlPhaseStartCleanup
        rlRun "vagrant destroy --force"
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
