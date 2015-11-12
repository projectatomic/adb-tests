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
