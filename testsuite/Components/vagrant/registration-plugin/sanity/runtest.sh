#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of vagrant/registration-plugin/sanity
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

# test needs this variables to be set:
#    vagrant_BOX_PATH ... path to vagrant box with RHEL
# and these variables are needed for test box registration
#    vagrant_RHN_USERNAME ... username for registration
#    vagrant_RHN_PASSWORD ... password for registration

rlJournalStart
    rlPhaseStartSetup
        rlImport 'testsuite/vagrant'
        vagrantBoxIsProvided || rlDie
        vagrantBoxAdd || rlDie
        vagrantPluginInstall vagrant-registration
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"
        rlRun "vagrant init $vagrant_BOX_NAME"
    rlPhaseEnd

    rlPhaseStartTest skip_registration
        vagrantConfigureGeneralVagrantfile "skip"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant halt"
    rlPhaseEnd

if vagrantRegistrationCredentialsProvided;then
    rlPhaseStartTest credentials_in_vagrantfile
        vagrantConfigureGeneralVagrantfile "file"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant ssh -c 'sudo subscription-manager status'"
        rlRun "vagrant ssh -c \"sudo sed -i 's/gpgcheck = [01]/gpgcheck = 0\nskip_if_unavailable=True/' /etc/yum.repos.d/redhat.repo\""  # workaround for sjis repo
        rlRun "vagrant ssh -c 'sudo yum install -y vim && sudo yum remove -y vim'"
        rlRun "vagrant halt"
    rlPhaseEnd

    rlPhaseStartTest credentials_from_environment
        vagrantConfigureGeneralVagrantfile "env"
        export USERNAME=$vagrant_RHN_USERNAME
        export PASSWORD=$vagrant_RHN_PASSWORD
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant ssh -c 'sudo subscription-manager status'"
        rlRun "vagrant ssh -c \"sudo sed -i 's/gpgcheck = [01]/gpgcheck = 0\nskip_if_unavailable=True/' /etc/yum.repos.d/redhat.repo\""  # workaround for sjis repo
        rlRun "vagrant ssh -c 'sudo yum install -y vim && sudo yum remove -y vim'"
        rlRun "vagrant halt"
    rlPhaseEnd
fi

    rlPhaseStartCleanup
        #vagrantBoxRemove # can be shared, so skipping
        rlRun "rm -f Vagrantfile"
        rlRun "rm -f ~/.vagrant.d/Vagrantfile"
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
