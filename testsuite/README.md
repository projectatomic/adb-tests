Description
===========
This is testsuite for testing CDK/ADB.


Testsuite structure
===================
Tests for specific part of CDK/ADB are in Componets/<component>
Code which could be shared between tests is in libraries under Library directory.
Libraries are documented with perlpod: http://perldoc.perl.org/perlpod.html.
This documentation can be transformed to various formats by tools,
for example pod2html, pod2markdown. Such exported documentation is in markdown format
in README.md file in directory of each library.
Code of tests should be as simple as possible and library functions as complex as needed.
Each test is suppose to be executed on host system. If some testing is needed in vagrant box,
there will be beakerlib test executed on host and it will care about executing code in box
(with library functions).


Test framework
==============
Tests are written in bash with beakerlib, open source bash library for testing:
https://fedorahosted.org/beakerlib/
Beakerlib was originally developed for rpm based linux systems,
but it can be used also on other systems, including OS X and Windows (in cygwin).
More detailed manual for installing beakerlib and dependencies
on various platforms will be provided later.

Beakerlib on Linux
------------------
TODO: howto install/use
Install Virtualbox and Vagrant

Beakerlib on Windows
--------------------
TODO: howto install/use
Install Virtualbox, Vagrant and cygwin (+ ssh, rsync)

Beakerlib on OS X
-----------------
TODO: howto install/use
Install Virtualbox and Vagrant
```bash
# brew install gnu-getopt
# brew install coreutils
```

How to run tests
================
Test can be executed by running runtest.sh and providing input as variables. More information about input values are in library testsuite/Library/vagrant/README
There is a plan for script which will execute all (relevent) tests and collect results, but currently
every test need to be executed directly by running runtest.sh, see several examples below.

On Linux
--------
```bash
#  vagrant_BOX_PATH=<path-to-vagrant-box> ./runtest.sh
```
```bash
#  vagrant_BOX_PATH=<path-to-vagrant-box> vagrant_RHN_USERNAME=<username> vagrant_RHN_PASSWORD=<password> ./runtest.sh
```

On Windows
----------
There are some differences on windows system, which is handled by library. It just need to know about it by setting HOST_PLATFORM.
```bash
#  vagrant_BOX_PATH=<path-to-vagrant-box> HOST_PLATFORM=win ./runtest.sh
```

On OS X
-------
On OS X, it's important to install and use gnu version of getopt, readlink and probably several more.
```bash
#  PATH="/usr/local/opt/coreutils/libexec/gnubin:/usr/local/Cellar/gnu-getopt/1.1.6/bin/:$PATH" vagrant_BOX_PATH=<path-to-vagrant-box> ./runtest.sh
```
