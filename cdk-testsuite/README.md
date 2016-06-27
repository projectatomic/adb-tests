
# Project :: Automation CDK(container Developement Kit)

This automation project it based on Avocado framework , Python 2.7 .It has ability to run on Mac OSX ,Windows , Fedora, CentOS and REHL

Few pre-requesites to run this project on your test machine

Install pexpect lib on your system (easy_install pexpect or pip install pexpect)




# How to run this project on Windows Machine


Install (tested in cygwin)

    For this you need to download the apt-cyg lib and paste this lib into your cygwin/bin( apt-cyg install python-setuptools python-yaml python-test)

    easy_install-2.7 pip

    pip install stevedore

    download and unpack sources from https://github.com/avocado-framework/avocado/releases

    python setup.py install



# How to run this project on Mac Machine



- root user enabled (by default is disabled)
 - System Integrity Protection (SIP aka rootless) feature enabled (default since El Captain)

So there are multiple ways how to use python on Mac, with SIP in El Captain
things get more complicated. But we do not want to require SIP disabled of course.
For a lot of details see eg.:
http://apple.stackexchange.com/questions/209572/how-to-use-pip-after-the-el-capitan-max-os-x-upgrade


first try with system installed python 2.7.10

$ mkdir avocado
$ cd avocado
$ git clone https://github.com/avocado-framework/avocado
$ cd avocado

 sudo -H easy_install pip  # probably not needed, next step should do it
 sudo make requirements

 -> need to comment these in requirements.txt
     - libvirt-python
     - pyliblzma
 -> need different six version then system installed
     - could be workaround, but I decided to try other ways first



/*RHEL ,CENTOS and fedora explaination pending*/
