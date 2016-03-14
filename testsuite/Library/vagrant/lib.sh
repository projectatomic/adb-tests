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

=over

=item vagrant_SHARING

This variable defines if library funcions can reuse some objects.
Currently, vagrant box and vagrant plugins can be shared.
Value can be `true` or `false`, default is `true`.

=back
=cut

vagrant_SHARING=${vagrant_SHARING:-"true"}

true <<'=cut'
=pod

=over

=item vagrant_BOX_NAME

Vagrant box name to be used by default by library functions.
Set it before usage of library functions.

=back
=cut

vagrant_BOX_NAME=${vagrant_BOX_NAME:-"cdkv2"}

true <<'=cut'
=pod

=over

=item vagrant_BOX_PATH

Path to file with vagrant box to be used by library functions.
Set it before usage of library functions.

=back

=over

=item vagrant_PLUGINS_DIR

Path to directory with vagrant plugins (*.gem) to install from.
If not provided, plugins are installed directly from upstream.

=back

=over

=item vagrant_VAGRANTFILE_DIRS

List of dirrectories with Vagrantfiles to test.
By default, new Vagrantfile is created,
but some test may want to test something over multiple prepared Vagrantfiles.

=back

=over

=item vagrant_RHN_USERNAME

Username for registration plugin.

=back

=over

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

=head2 vagrantBoxIsProvided

Check if file with vagrant box is provided. Path to vagrant box is expected in variable vagrant_BOX_PATH.

    vagrantBoxIsProvided

=over

=back

Returns 0 when the plugin is path to vagrant is provided and valid, non-zero otherwise.
If vagrant_SHARING is true, function also return 0 if vagrant already contain box vagrant_BOX_NAME.

=cut

vagrantBoxIsProvided() {
        if [ "$vagrant_SHARING" == "true" ]; then
            vagrant box list | grep "$vagrant_BOX_NAME" && return 0
        fi
        if [ "$vagrant_BOX_PATH" == "" ] ; then
            if [ "$vagrant_SHARING" == "true" ]; then
                rlLogFatal "Variable vagrant_BOX_PATH is empty and box $vagrant_BOX_NAME is not already added."
            else
                rlLogFatal "Variable vagrant_BOX_PATH is empty and sharing is not enabled."
            fi
            return 1
        fi
        rlAssertExists $vagrant_BOX_PATH
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantBoxAdd

Add vagrant box (path in VAGRANT_BOX_PATH).

    vagrantBoxAdd [--force]

=over

Add vagrant box. If vagrant_SHARING is true, box is added only if not present.
If vagrant_SHARING is false or parametr `--force` is added, vagrant box is removed first if already present.

=back

Returns 0 when te vagrant box is successfully added, non-zero otherwise.

=cut

vagrantBoxAdd() {
    if [ "$vagrant_SHARING" == "false" -o "$1" == "--force" ]; then
        vagrantBoxRemove || return 1
    fi
    vagrant box list | grep $vagrant_BOX_NAME && return 0
    rlRun "vagrant box add --name $vagrant_BOX_NAME $vagrant_BOX_PATH"
    vagrant box list | grep $vagrant_BOX_NAME || rlFail "vagrant box was not added correctly"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantBoxRemove

Remove vagrant box (with name from vagrant_BOX_NAME variable).

    vagrantBoxRemove

=over

=back

Returns 0 when te vagrant box is successfully removed, non-zero otherwise.

=cut

vagrantBoxRemove() {
    rlRun "vagrant box remove --force $vagrant_BOX_NAME"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantPluginInstall

Install a vagrant plugin with given name.
If vagrant SHARING is false or parameter `--force` is given,
plugin is uninstalled first.
Plugin will be installed from vagrant_PLUGINS_DIR if defined and from upstream otherwise.

    vagrantPluginInstall name [--force]

=over

=item name

Vagrant plugin name.

=item --force

Enfoce reinstalling plugin.

=back

Returns 0 when the plugin is successfully installed, non-zero otherwise.

=cut

vagrantPluginInstall() {
    # we need one parameter with name + optional '--force'
    [ $# -eq 1 ] || [ $# -eq 2 -a "$2" == "--force" ] || { rlFail 'Wrong usage'; return 1; }
    if [ "$2" == "--force" -o "$vagrant_SHARING" == "false" ];then
        # uninstall plugin first if needed
        if `vagrant plugin list | grep $1`;then
            vagrantPluginUninstall $1
        fi
    fi

    # skip if sharing enabled and plugin already installed
    if [ "$vagrant_SHARING" == "true" ] && vagrant plugin list | grep $1; then
        rlLog "Plugin $1 already installed, installation skipped."
    else
        # install itself
        if [ "$vagrant_PLUGINS_DIR" != "" ]; then
            rlRun "vagrant plugin install $vagrant_PLUGINS_DIR/${1}*.gem"
        else
            rlRun "vagrant plugin install $1"
        fi
    fi

    rlLogInfo "Plugin `vagrant plugin list | grep $1` installed"
    # final check
    vagrant plugin list | grep $1

    return $?
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantPluginUninstall

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
    if `vagrant plugin list | grep $1`; then
        rlRun "vagrant plugin uninstall $1"
        vagrant plugin list | grep $1 && rlFail "Plugin uninstall failed"
        [ $? -ne 1 ] && return 1
    else
        rlLogDebug "Plugin not installed"
    fi
    return 0
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantRegistrationCredentialsProvided

Check if registration credentials are provided in variables vagrant_RHN_USERNAME and vagrant_RHN_PASSWORD

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantBoxHostname

Connects to box and print it's hostname.

    vagrantBoxHostname

=over

=back

=cut

vagrantBoxHostname() {
        hostname=`vagrant ssh -c "hostname" | grep -o '\b.*\b'`
        echo "$hostname"
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

true <<'=cut'
=pod

=head2 vagrantConfigureGeneralVagrantfile 

Configure main Vagrantfile (in ~/.vagrant.d).

    vagrantConfigureGeneralVagrantfile type

=over

=item type

skip: skip box registration

file: credentials in general Vagrantfile

env: credentials in variables SUB_USERNAME and SUB_PASSWORD

=back

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
        rm -f $generalVagrantfile
        echo 'ENV["VAGRANT_DETECTED_OS"] = ENV["VAGRANT_DETECTED_OS"].to_s + " cygwin"' >> $generalVagrantfile
    else
        rm -f $generalVagrantfile
    fi
    vagrant plugin list
    vagrant plugin list | grep registration
    if vagrant plugin list | grep registration; then
        HAS_REG_PLUGIN=true
    else
        HAS_REG_PLUGIN=false
    fi
    echo "Vagrant.configure('2') do |config|" >> $generalVagrantfile
    if $HAS_REG_PLUGIN;then
        case $1 in
            skip)
                echo "config.registration.skip = true" >> $generalVagrantfile
                ;;
            file)
                if [ "$vagrant_RHN_SERVER_URL" != "" ]; then
                    echo "config.registration.serverurl = 'https://$vagrant_RHN_SERVER_URL/subscription/'" >> $generalVagrantfile
                fi
                echo "config.registration.username = '$vagrant_RHN_USERNAME'" >> $generalVagrantfile
                echo "config.registration.password = '$vagrant_RHN_PASSWORD'" >> $generalVagrantfile
                ;;
            env)
                echo "config.registration.serverurl = ENV['SERVERURL']" >> $generalVagrantfile
                echo "config.registration.username = ENV['SUB_USERNAME']" >> $generalVagrantfile
                echo "config.registration.password = ENV['SUB_PASSWORD']" >> $generalVagrantfile
                ;;
            *)
                echo "ERROR: unexpected argument '$1' for function registration_plugin_configure"
                ;;
        esac
    fi
    echo "end" >> $generalVagrantfile
    return
}

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

=item *

Ondrej Ptak <optak@redhat.com>

=back

=cut
