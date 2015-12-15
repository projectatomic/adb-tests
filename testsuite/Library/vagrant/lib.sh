#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   lib.sh of /Library/vagrant
#   Description: Library for common vagrant operations
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
#   library-prefix = vagrant
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 NAME

vagrant - Library for common vagrant operations

=head1 DESCRIPTION

This is a library for common tasks done with Vagrant.
It wraps various vagrant commands with relevant asserts.

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

=item vagrant_VERSION

Info about installed version of Vagrant (vagrant -v). 

=item vagrant_PROVIDER

Vagrant provider to be used: kvm, virtualbox or vmware.
Set it before usage of library functions.

=back

=cut

vagrant_PROVIDER=${vagrant_PROVIDER:-"virtualbox"}

true <<'=cut'
=pod

=item vagrant_BOX_NAME

Vagrant box name to be used by default by library functions.
Set it before usage of library functions.

=back
=cut

vagrant_BOX_NAME=${vagrant_BOX_NAME:-"cdkv2"}

true <<'=cut'
=pod

=item vagrant_BOX_PATH

Path to file with vagrant box to be used by library functions.
Set it before usage of library functions.

=back


=item vagrant_RHN_USERNAME

Username for registration plugin.

=back

=item vagrant_RHN_PASSWORD

Password for registration plugin.

=back
=cut

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 FUNCTIONS

=head2

Install a vagrant plugin (uninstall first when needed).

    vagrantPluginInstall name_or_file_path

=over

=item name_or_file_path

Vagrant plugin name (remote install) or file path (local install)

=back

Returns 0 when the plugin is successfully installed, non-zero otherwise.

=cut

vagrantPluginInstall() {
    # we need exactly one parameter
    [ $# -ne 1 ] && { rlFail 'Wrong usage'; return 1; }

    # get name from argument (strip postfix for file paths)
    local name
    name=$(echo $1 | sed 's/.*\/\(.*\)-[0-9]\.[0-9]\.[0-9]\.gem$/\1/')
    
    # uninstall if needed
    if vagrant plugin list | grep $name; then
        rlRun "vagrant plugin uninstall $name" 0,1
        rlRun "vagrant plugin list | grep $name" 1 "Plugin uninstalled successfully"
    fi

    # install itself 
    rlRun "vagrant plugin install $1"

    # final check
    rlRun "vagrant plugin list | grep $name"

    return $?
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2

Uninstall a vagrant plugin

    vagrantPluginUninstall name

=over

=item name

Vagrant plugin name to uninstall

=back

Returns 0 when the plugin is successfully uninstalled, non-zero otherwise.

=cut

vagrantPluginUninstall() {
    # we need exactly one parameter
    [ $# -ne 1 ] && { rlFail 'Wrong usage'; return 1; };

    # uninstall 
    if $(vagrant plugin list | grep $1); then
        rlRun "vagrant plugin uninstall $1"
        rlRun "vagrant plugin list | grep $1" 1 "Plugin uninstalled successfully"
        [ $? -ne 1 ] && return 1
    else
        rlLogDebug "Plugin not installed"
    fi
    return 0
}

true <<'=cut'
=pod

=head2

Check if file with vagrant box is provided. Path to vagrant box is expected in variable VAGRANT_BOX_PATH

    vagrantBoxIsProvided

=over

=back

Returns 0 when the plugin is path to vagrant is provided, non-zero otherwise.

=cut

vagrantBoxIsProvided() {
        if [ "$vagrant_BOX_PATH" == "" ]; then
            rlLogError "variable vagrant_BOX_PATH is empty"
            return 1
        fi
        rlAssertExists $vagrant_BOX_PATH
}


true <<'=cut'
=pod

=head2

Check if file with vagrant box is provided

    vagrantRegistrationCredentialsProvided

=over

=back

Returns 0 when the username and password for registration plugin are provided, non-zero otherwise.

=cut

vagrantRegistrationCredentialsProvided() {
        # RHN_USER
        if [ "$vagrant_RHN_USERNAME" == "" ]; then
            rlLogError "variable vagrant_RHN_USERNAME is empty"
            return 1
        fi
        # RHN_PASS
        if [ "$vagrant_RHN_PASSWORD" == "" ]; then
            rlLogError "variable vagrant_RHN_PASSWORD is empty"
            return 1
        fi
}

true <<'=cut'
=pod

=head2

Add vagrant box (path in VAGRANT_BOX_PATH).

    vagrantBoxAdd

=over

=back

Returns 0 when te vagrant box is successfully added, non-zero otherwise.

=cut

vagrantBoxAdd() {
    vagrant box list | grep "There are no installed boxes"
    if [ $? == 1 ]; then
        rlLogFatal "there are currently some vagrant boxes, remove them before runing this script"
        exit 1
    fi
    rlRun "vagrant box add --name $vagrant_BOX_NAME $vagrant_BOX_PATH"
    vagrant box list | grep $vagrant_BOX_NAME || rlFail "vagrant box was not added correctly"
}

true <<'=cut'
=pod

=head2

Remove vagrant box (with name from vagrant_BOX_NAME variable)

    vagrantBoxRemove

=over

=back

Returns 0 when te vagrant box is successfully removed, non-zero otherwise.

=cut

vagrantBoxRemove() {
    rlRun "vagrant box remove --force $vagrant_BOX_NAME"
}

true <<'=cut'
=pod

=head2

Configure main Vagrantfile (in ~/.vagrant.d).

    vagrantConfigureGeneralVagrantfile type

=over

=item type

=back

# TODO: update || remove
Returns 0 when te vagrant box is successfully removed, non-zero otherwise.

=cut

vagrantConfigureGeneralVagrantfile () {
    # takes one argument: skip, file, or env
    # TODO: to be extended when we will need to configure more than registratino plugin && win workaround
    if [ $# != 1 ]; then
        rlFail "wrong number of argument, use single one: {skip,file,env}"
    fi
    generalVagrantfile=~/.vagrant.d/Vagrantfile
    if [ "$HOST_PLATFORM" == "win" ]; then
        # workaround for windows host
        generalVagrantfile="c:\\Users\\$LOGNAME\\.vagrant.d\\Vagrantfile"
        generalVagrantfile="/cygdrive/c/Users/$USER/.vagrant.d/Vagrantfile"
        rm -f $reneralVagrantfile
        echo 'ENV["VAGRANT_DETECTED_OS"] = ENV["VAGRANT_DETECTED_OS"].to_s + " cygwin"' >> $generalVagrantfile
    else
        rm -f $reneralVagrantfile
    fi
    echo "Vagrant.configure('2') do |config|" > $generalVagrantfile
    # TODO: add WIN workaround if needed -> how to know test is running on windows?
    case $1 in
        skip)
            echo "config.registration.skip = true" >> $generalVagrantfile
            ;;
        file)
            echo "config.registration.username = '$vagrant_RHN_USERNAME'" >> $generalVagrantfile
            echo "config.registration.password = '$vagrant_RHN_PASSWORD'" >> $generalVagrantfile
            ;;
        env)
            echo "config.registration.username = ENV['USERNAME']" >> $generalVagrantfile
            echo "config.registration.password = ENV['PASSWORD']" >> $generalVagrantfile
            ;;
        *)
            echo "ERROR: unexpected argument '$1' for function registration_plugin_configure"
            ;;
    esac
    echo "end" >> $generalVagrantfile
    return
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Verification
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   This is a verification callback which will be called by
#   rlImport after sourcing the library to make sure everything is
#   all right. It makes sense to perform a basic sanity test and
#   check that all required packages are installed. The function
#   should return 0 only when the library is ready to serve.

vagrantLibraryLoaded() {
    if vagrant_VERSION=$(vagrant -v); then
        rlPass "$vagrant_VERSION is present, vagrant library should work."
        return 0
    else
        rlLogError "Vagrant seems not to be present!"
        return 1
    fi
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Authors
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head1 AUTHORS

=over

=item *

David Kutalek <dkutalek@redhat.com>
Ondrej Ptak <optak@redhat.com>

=back

=cut
