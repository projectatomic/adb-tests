ADB + Eclipse with vagrant-adbinfo plugin
=========================================

- create your workspace `mkdir -p ~/adb-eclipse && cd ~/adb-eclipse`
- `vagrant plugin install vagrant-adbinfo`

-  Export following into a `Vagrantfile`
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

#Vagrant file for libvirt/kvm and virtualbox provider

Vagrant.configure(2) do |config|
  config.vm.box = "atomicapp/dev"

  config.vm.network "forwarded_port", guest: 2376, host: 2379, auto_correct: true
  config.vm.provider "libvirt" do |libvirt, override|
    libvirt.driver = "kvm"
    libvirt.memory = 1024
    libvirt.cpus = 2
  end

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
export DOCKER_CERT_PATH=/root/vagrant/adb/.vagrant/machines/default/virtualbox/.docker
export DOCKER_TLS_VERIFY=1
export DOCKER_MACHINE_NAME="8606567"
```

- Details about the vagrant box is displayed as part of the output
- To test the client connection to `docker` daemon inside CDK: In the Vagrantfile at line no: 7, we have mapped host port `2379` to `docker` daemon port (2376) inside CDK, which means that you can access the daemon at (host machine) 127.0.0.1:2379.
  Following is an example of connecting via `docker` CLI to daemon over TLS enabled TCP connection
  
  ```bash
  # copy the certs (generated above) to proper place where `docker` (by default) look up
  cp -r *.pem  ~/.docker
  docker -H 127.0.0.1:2379 --tlsverify images
  ```

- To test out the connection with Eclipse kindly check <https://www.eclipse.org/community/eclipse_newsletter/2015/june/article3.php> and this Video by Xavier Coulon <https://www.youtube.com/watch?v=RUgEgtLux8Q>. More Eclipse Docker Tooling documentations are at <<https://wiki.eclipse.org/Linux_Tools_Project/Docker_Tooling/User_Guide>>
