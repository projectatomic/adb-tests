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

- vagrant\_SHARING

    This variable defines if library funcions can reuse some objects.
    Currently, vagrant box and vagrant plugins can be shared.
    Value can be \`true\` or \`false\`, default is \`true\`.

- vagrant\_BOX\_NAME

    Vagrant box name to be used by default by library functions.
    Set it before usage of library functions.

- vagrant\_BOX\_PATH

    Path to file with vagrant box to be used by library functions.
    Set it before usage of library functions.

- vagrant\_PLUGINS\_DIR

    Path to directory with vagrant plugins (\*.gem) to install from.
    If not provided, plugins are installed directly from upstream.

- vagrant\_VAGRANTFILE\_DIRS

    List of dirrectories with Vagrantfiles to test.
    By default, new Vagrantfile is created,
    but some test may want to test something over multiple prepared Vagrantfiles.

- vagrant\_RHN\_USERNAME

    Username for registration plugin.

- vagrant\_RHN\_PASSWORD

    Password for registration plugin.

# FUNCTIONS

## vagrantBoxIsProvided

Check if file with vagrant box is provided. Path to vagrant box is expected in variable vagrant\_BOX\_PATH.

    vagrantBoxIsProvided

Returns 0 when the plugin is path to vagrant is provided and valid, non-zero otherwise.
If vagrant\_SHARING is true, function also return 0 if vagrant already contain box vagrant\_BOX\_NAME.

## vagrantBoxAdd

Add vagrant box (path in VAGRANT\_BOX\_PATH).

    vagrantBoxAdd [--force]

> Add vagrant box. If vagrant\_SHARING is true, box is added only if not present.
> If vagrant\_SHARING is false or parametr \`--force\` is added, vagrant box is removed first if already present.

Returns 0 when te vagrant box is successfully added, non-zero otherwise.

## vagrantBoxRemove

Remove vagrant box (with name from vagrant\_BOX\_NAME variable).

    vagrantBoxRemove

Returns 0 when te vagrant box is successfully removed, non-zero otherwise.

## vagrantPluginInstall

Install a vagrant plugin with given name.
If vagrant SHARING is false or parameter \`--force\` is given,
plugin is uninstalled first.
Plugin will be installed from vagrant\_PLUGINS\_DIR if defined and from upstream otherwise.

    vagrantPluginInstall name [--force]

- name

    Vagrant plugin name.

- --force

    Enfoce reinstalling plugin.

Returns 0 when the plugin is successfully installed, non-zero otherwise.

## vagrantPluginUninstall

Uninstall a vagrant plugin

    vagrantPluginUninstall name

- name

    Vagrant plugin name to uninstall

Returns 0 when the plugin is successfully uninstalled, non-zero otherwise.

## vagrantRegistrationCredentialsProvided

Check if registration credentials are provided in variables vagrant\_RHN\_USERNAME and vagrant\_RHN\_PASSWORD

    vagrantRegistrationCredentialsProvided

Returns 0 when the username and password for registration plugin are provided, non-zero otherwise.

## vagrantBoxHostname

Connects to box and print it's hostname.

    vagrantBoxHostname

## vagrantConfigureGeneralVagrantfile 

Configure main Vagrantfile (in ~/.vagrant.d).

    vagrantConfigureGeneralVagrantfile type

- type

    skip: skip box registration

    file: credentials in general Vagrantfile

    env: credentials in variables SUB\_USERNAME and SUB\_PASSWORD

# AUTHORS

- David Kutalek <dkutalek@redhat.com>
- Ondrej Ptak <optak@redhat.com>
