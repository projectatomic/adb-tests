#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of vagrant/service-manager/sanity
#   Description: test service-manager vagrant plugin
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
        rlImport 'testsuite/vagrant'
        vagrantBoxIsProvided || rlDie
        vagrantBoxAdd || rlDie
        vagrantPluginInstall vagrant-service-manager
        vagrantConfigureGeneralVagrantfile skip
    rlPhaseEnd

for dir in $vagrant_VAGRANTFILE_DIRS;do
    rlPhaseStartTest testing_with_$dir
        #rhel-ose_found=false
        #for dir in $vagrant_VAGRANTFILE_DIRS; do
        #    if `echo $dir | grep "rhel-ose$"`; then
        #        rhel-ose_found=true
        #        break
        #    fi
        #done
        #if [ "$rhel-ose_found" == false ]; then
        #    rlDie "test do not have Vagrantfile for rhel-ose
        rlRun "pushd $dir"
        rlLogInfo "Testing without running VM"
        rlRun "vagrant service-manager env docker > stdout 2> stderr" 1-255
        echo -e "stdout:\n========"
        cat stdout
        echo -e "stderr:\n========"
        cat stderr
        echo "========"
        rlAssertNotGrep '.' stdout
        #rlAssertGrep "target machine is required to run" stderr
        rlAssertGrep "The virtual machine must be running before you execute this command." stderr

        rlLogInfo "Testing with running VM"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant service-manager env docker > stdout 2> stderr"
        echo -e "stdout:\n========"
        cat stdout
        echo -e "stderr:\n========"
        cat stderr
        echo "========"
        rlAssertNotGrep "." stderr
        rlAssertGrep "DOCKER_HOST=tcp://[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*:[0-9]*" stdout
        rlAssertGrep "DOCKER_CERT_PATH=.*\.docker" stdout
        rlAssertGrep "DOCKER_TLS_VERIFY=1" stdout
        rlAssertGrep "DOCKER_MACHINE_NAME=[0-9a-f]*" stdout
        rlAssertGrep 'eval "$(vagrant adbinfo)' stdout

        rlRun "vagrant destroy -f"
        rlRun "popd"
    rlPhaseEnd
done

    rlPhaseStartCleanup
        #vagrantBoxRemove # can be shared, so skipping
        rlRun "rm -f ~/.vagrant.d/Vagrantfile"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
