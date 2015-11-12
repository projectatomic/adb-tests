ADB + Eclipse with vagrant-adbinfo plugin on Windows
=====================================================

Following are the steps to setup [ADB] (https://github.com/projectatomic/adb-atomic-developer-bundle/) on Windows Operating system.

Note: Following steps are tested on Windows 7.

- Install vagrant -  Guide <http://www.vagrantup.com/downloads>

- Install VirtualBox 5.0.8 - Guide <https://www.virtualbox.org/wiki/Downloads>

- Download Eclipse <https://eclipse.org/downloads/> and install the Docker tooling plugin <http://www.eclipse.org/community/eclipse_newsletter/2015/june/article3.php>

- Download the `pscp` from [here](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
  - Save pscp.exe somewhere on your hard drive. `C:\Windows\` is a good location in the default execution path.

- Install the vagrant-adbinfo plugin `vagrant plugin install vagrant-adbinfo` OR update using `vagrant plugin update vagrant-adbinfo` accordingly.

-  Export following into a `Vagrantfile`
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

#Vagrant file for libvirt/kvm and virtualbox provider

Vagrant.configure(2) do |config|
  config.vm.box = "atomicapp/dev"

  config.vm.network "forwarded_port", guest: 2376, host: 2379, auto_correct: true

  config.vm.provider "virtualbox" do |vbox, override|
    vbox.memory = 1024
    vbox.cpus = 2

    # Enable use of more than one virtual CPU in a virtual machine.
    vbox.customize ["modifyvm", :id, "--ioapic", "on"]
  end

end
```
- Run `vagrant up --provider virtualbox` (in the same directory where Vagrantfile exist)

- Run `vagrant adbinfo` in your current working directory

```
$ vagrant adbinfo
Set the following environment variables to enable access to the
docker daemon running inside of the vagrant virtual machine:

export DOCKER_HOST=tcp://127.0.0.1:2379
export DOCKER_CERT_PATH=c:\Users\nshaikh\vagrant-adbinfo\.vagrant\machines\default\virtualbox\.docker\
export DOCKER_TLS_VERIFY=1
export DOCKER_MACHINE_NAME=8606567
```

- Connection details for the `docker` daemon inside ADB are displayed after executing the vagrant adbinfo plugin

- To test the client connection to `docker` daemon inside ADB: In the Vagrantfile, we have mapped host port `2379` to `docker` daemon port (2376) inside ADB, which means that you can access the daemon at (host machine) 127.0.0.1:2379.

- To test out the connection with Eclipse kindly check <https://www.eclipse.org/community/eclipse_newsletter/2015/june/article3.php> and this Video by Xavier Coulon <https://www.youtube.com/watch?v=RUgEgtLux8Q>. More Eclipse Docker Tooling documentations are at <<https://wiki.eclipse.org/Linux_Tools_Project/Docker_Tooling/User_Guide>>
