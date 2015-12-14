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

=back

=cut
