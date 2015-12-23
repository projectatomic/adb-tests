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
        # configure general Vagrantfile,
        #   mainly for cygwin workaround for windows
        vagrantConfigureGeneralVagrantfile "skip"
    rlPhaseEnd

    rlPhaseStartTest remote_install
        vagrant_PLUGINS_DIR='' vagrantPluginInstall vagrant-adbinfo --force
        # run without running vm (fast smoke)
        rlRun "vagrant adbinfo 2>&1 | grep 'target machine is required to run'"
    rlPhaseEnd

  if [ "$vagrant_PLUGINS_DIR" != "" ];then
    # vagrant_PLUGINS_DIR provided, test also local install of plugin
    rlPhaseStartTest local_install
        vagrantPluginInstall vagrant-adbinfo --force
        # run without running vm (fast smoke)
        rlRun "vagrant adbinfo 2>&1 | grep 'target machine is required to run'"
    rlPhaseEnd
  fi

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
