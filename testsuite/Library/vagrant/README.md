# NAME

vagrant - Library for common vagrant operations

# DESCRIPTION

This is a library for common tasks done with Vagrant.
It wraps various vagrant commands with relevant asserts.

# VARIABLES

There are a few input variables you can use to pass settings to this Library,
and also other variables where you can find results of called functions.

- vagrant\_VERSION

    Info about installed version of Vagrant (vagrant -v). 

- vagrant\_PROVIDER

    Vagrant provider to be used: kvm, virtualbox or vmware.
    Set it before usage of library functions.

- vagrant\_BOX\_NAME

    Vagrant box name to be used by default by library functions.
    Set it before usage of library functions.

- vagrant\_BOX\_PATH

    Path to file with vagrant box to be used by library functions.
    Set it before usage of library functions.

- vagrant\_RHN\_USERNAME

    Username for registration plugin.

- vagrant\_RHN\_PASSWORD

    Password for registration plugin.

# FUNCTIONS

## vagrantBoxIsProvided

Check if file with vagrant box is provided. Path to vagrant box is expected in variable VAGRANT\_BOX\_PATH.

    vagrantBoxIsProvided

Returns 0 when the plugin is path to vagrant is provided and valid, non-zero otherwise.

## vagrantBoxAdd

Add vagrant box (path in VAGRANT\_BOX\_PATH).

    vagrantBoxAdd

Returns 0 when te vagrant box is successfully added, non-zero otherwise.

## vagrantBoxRemove

Remove vagrant box (with name from vagrant\_BOX\_NAME variable).

    vagrantBoxRemove

Returns 0 when te vagrant box is successfully removed, non-zero otherwise.

## vagrantPluginInstall

Install a vagrant plugin (uninstall first when needed).

    vagrantPluginInstall name_or_file_path

- name\_or\_file\_path

    Vagrant plugin name (remote install) or file path (local install).

Returns 0 when the plugin is successfully installed, non-zero otherwise.

## vagrantPluginUninstall

Uninstall a vagrant plugin

    vagrantPluginUninstall name

- name

    Vagrant plugin name to uninstall

Returns 0 when the plugin is successfully uninstalled, non-zero otherwise.

## vagrantRegistrationCredentialsProvided

Check if file with vagrant box is provided in variables vagrant\_RHN\_USERNAME and vagrant\_RHN\_PASSWORD

    vagrantRegistrationCredentialsProvided

Returns 0 when the username and password for registration plugin are provided, non-zero otherwise.

## vagrantConfigureGeneralVagrantfile 

Configure main Vagrantfile (in ~/.vagrant.d).

    vagrantConfigureGeneralVagrantfile type

- type

    skip: skip box registration

    file: credentials in general Vagrantfile

    env: credentials in variables USERNAME and PASSWORD

# AUTHORS

- David Kutalek <dkutalek@redhat.com>
- Ondrej Ptak <optak@redhat.com>
