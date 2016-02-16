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
#    vagrant_RHN_SERVER_URL ... server for registration

vagrant_RHN_SERVICE_URL="https://$vagrant_RHN_SERVER_URL/subscription"

set -o pipefail

# get identity and status (from inside vagrant box)
# $1 - prefix to store these info
get_subscription_id() {
    rlLog "Getting subscription id ($1)"
    rlRun "vagrant ssh -c 'sudo subscription-manager identity' > $1-identity.txt"
    rlRun "vagrant ssh -c 'sudo subscription-manager status' > $1-status.txt"
    rlRun "vagrant ssh -c 'sudo subscription-manager list --consumed' > $1-list-consumed.txt"
    rlRun "vagrant ssh -c 'sudo subscription-manager facts' > $1-facts.txt"

    # parse identity
    CONSUMER_UUID=$(cat $1-identity.txt | grep -i identity | sed 's/.*: *\(.*\)/\1/' | tr -d '\r\n')
    rlLog "CONSUMER_UUID=$CONSUMER_UUID"
}

# get consumer info and entitlements (from host, not vagrant box)
# $1 - prefix to store these info
get_subscription_info() {
    test -z $CONSUMER_UUID && { rlFail "Getting subscription info: CONSUMER_UUID not known!"; return; }
    rlLog "Getting subscription info ($1, $CONSUMER_UUID)"
    # get consumer subscription info
    rlRun "curl -k -u '$vagrant_RHN_USERNAME:$vagrant_RHN_PASSWORD' '$vagrant_RHN_SERVICE_URL/consumers/$CONSUMER_UUID' | python -mjson.tool > $1-consumer.txt"
    # get entitlement info
    rlRun "curl -k -u '$vagrant_RHN_USERNAME:$vagrant_RHN_PASSWORD' '$vagrant_RHN_SERVICE_URL/consumers/$CONSUMER_UUID/entitlements' | python -mjson.tool > $1-entitlements.txt"
}

# check that SKU in facts and one actually consumed matches
# $1 - facts file name
# $2 - consumed file name
# $3 - entitlement file name
check_sku() {
    FACTS_SKU=$(cat $1 | grep dev_sku | sed 's/.*: *//' | tr -d '\r\n')
    rlLog "Facts SKU:    '$FACTS_SKU'"
    CONSUMED_SKU=$(cat $2 | grep SKU | sed 's/.*: *//' | tr -d '\r\n')
    rlLog "Consumed SKU: '$CONSUMED_SKU'"
    rlRun "test '_$FACTS_SKU' = '_$CONSUMED_SKU'"
    rlAssertEquals "Exactly one developmentPool in entitlements." $(grep developmentPool $3 | wc -l) 1
    rlRun "grep 'developmentPool.*true' $3"
}

rlJournalStart
    rlPhaseStartSetup
        rlImport 'testsuite/vagrant'
        vagrantBoxIsProvided || rlDie
        vagrantBoxAdd || rlDie
        vagrantPluginInstall vagrant-registration
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"
        rlRun "vagrant init $vagrant_BOX_NAME"
        cat ./Vagrantfile
    rlPhaseEnd

    rlPhaseStartTest skip_registration
        vagrantConfigureGeneralVagrantfile "skip"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant halt"
    rlPhaseEnd

# rest of test phases needs credentials
if vagrantRegistrationCredentialsProvided;then

    rlPhaseStartTest manual_registration
        # note: running the box still without registration via plugin (skip in general vagrant file)
        rlRun "vagrant up"
        rlRun "vagrant ssh -c 'ls -l /etc/rhsm/facts/ /etc/pki/product/'"
        rlRun "time vagrant ssh -c 'sudo subscription-manager register --username $vagrant_RHN_USERNAME --password $vagrant_RHN_PASSWORD --serverurl $vagrant_RHN_SERVER_URL --auto-attach' > register.txt"
        get_subscription_id   'manual'
        get_subscription_info 'manual'

        check_sku "manual-facts.txt" "manual-list-consumed.txt" "manual-entitlements.txt"

        rlRun "time vagrant ssh -c 'sudo subscription-manager remove --all'"
        get_subscription_info 'manual-removed'
        rlRun "grep '\[\]' manual-removed-entitlements.txt"
        rlAssertEquals "No entitlements after 'remove --all'" $(cat manual-removed-entitlements.txt | wc -l) 1

        rlRun "time vagrant ssh -c 'sudo subscription-manager unregister'"
        rlRun "vagrant ssh -c 'sudo subscription-manager identity' > manual-unregistered-identity.txt" 1
        rlRun "vagrant ssh -c 'sudo subscription-manager status' > manual-unregistered-status.txt" 1
        get_subscription_info 'manual-unregistered'
        rlRun "cat manual-unregistered-status.txt"

        rlRun "vagrant halt"
    rlPhaseEnd

    rlPhaseStartTest plugin_registration
        vagrantConfigureGeneralVagrantfile "file"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        get_subscription_id   'plugin'
        get_subscription_info 'plugin'

        check_sku "plugin-facts.txt" "plugin-list-consumed.txt" "plugin-entitlements.txt"

        rlRun "vagrant halt"
        get_subscription_info 'plugin-halted'
        rlRun "grep '\[\]' plugin-halted-entitlements.txt"
        rlAssertEquals "No entitlements after halt'" $(cat plugin-halted-entitlements.txt | wc -l) 1

        rlRun "vagrant destroy --force"
        get_subscription_info 'plugin-destroyed'
        rlRun "grep '\[\]' plugin-destroyed-entitlements.txt"
        rlAssertEquals "No entitlements after destroy'" $(cat plugin-destroyed-entitlements.txt | wc -l) 1
    rlPhaseEnd

    rlPhaseStartTest credentials_in_vagrantfile
        vagrantConfigureGeneralVagrantfile "file"
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant ssh -c 'sudo subscription-manager status'"
        rlRun "vagrant ssh -c \"sudo sed -i 's/gpgcheck = [01]/gpgcheck = 0\nskip_if_unavailable=True/' /etc/yum.repos.d/redhat.repo\""  # workaround for sjis repo
        rlRun "vagrant ssh -c 'sudo yum install -y nano && sudo yum remove -y nano'"
        rlRun "vagrant halt"
    rlPhaseEnd

    rlPhaseStartTest credentials_from_environment
        vagrantConfigureGeneralVagrantfile "env"
        export SERVERURL=$vagrant_SERVICE_URL # intentionally SERVICE_URL here
        export SUB_USERNAME=$vagrant_RHN_USERNAME
        export SUB_PASSWORD=$vagrant_RHN_PASSWORD
        rlRun "vagrant up --provider $vagrant_PROVIDER"
        rlRun "vagrant ssh -c 'echo hello' | grep hello"
        rlRun "vagrant ssh -c 'sudo subscription-manager status'"
        rlRun "vagrant ssh -c \"sudo sed -i 's/gpgcheck = [01]/gpgcheck = 0\nskip_if_unavailable=True/' /etc/yum.repos.d/redhat.repo\""  # workaround for sjis repo
        rlRun "vagrant ssh -c 'sudo yum install -y nano && sudo yum remove -y nano'"
        rlRun "vagrant halt"
    rlPhaseEnd
fi

    rlPhaseStartCleanup
        rlRun "vagrant destroy --force"
        #vagrantBoxRemove # can be shared, so skipping
        rlRun "rm -f ~/.vagrant.d/Vagrantfile"
        rlRun "popd"
        rlRun "rlBundleLogs registration-plugin-outputs $TmpDir/*"
        #rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
