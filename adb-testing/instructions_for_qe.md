Test cases for ADB and Eclipse integration using vagrant-adbinfo
================================================================

This document enlist the test cases for testing integration of ADB and Eclipse Docker tooling plugin.

Setup environment for testing
-----------------------------

- Setup ADB - <https://github.com/projectatomic/adb-atomic-developer-bundle/blob/master/docs/installing.rst>

- Setup vagrant-adbinfo plugin and Eclipse on the given operating system - https://github.com/navidshaikh/testing-adb

Test cases
----------

- vagrant plugin installation: The vagrant plugin installation should not issue any warning or conflict

- vagrant plugin update: If the vagrant plugin is already installed, the update of vagrant plugin should not issue any warning.
  To update a plugin run `vagrant plugin update vagrant-adbinfo`

- vagrant plugin command line: 
  - Create a workspace directory and export following contents in a Vagrantfile

```
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

  - Once box is up and running, run `vagrant adbinfo`
  - The execution of the plugin does following - 
     - Copies the client side certs from inside the ADB to host machine
     - Finds the port where Docker daemon port inside ADB is forwarded on the host machine
     - Finds the machine id

- Verify the `.docker` directory in the secrets path: 
  - Plugin creates a new directory `.docker` in `.vagrant/machines/default/virtualbox/` directory relative to your Vagrantfile location
  - Plugin copies the certs (`ca.pem, cert.pem, key.pem`) in `.vagrant/machines/default/virtualbox/.docker/` directory
  - Verify the path is absolute and correct

- Verify the Docker daemon forwarded port:
  In Vagrantfile, we mentioned guest port `2376` to be forwarded to host port `2379`, verify it the plugin output, the DOCKER_HOST variable value should be `tcp://127.0.0.1:2379`

- Verify the machine id:
  Run `vagrant global-status` and verify the machine `id` mentioned in the output is same as the one displayed in the plugin output by variable `DOCKER_MACHINE_NAME`

- Verify the integration with Eclipse: Now lets connect to Eclipse Docker plugin using the connection details displayed by the plugin
  - Verify that you have installed the Docker Tooling plugin in Eclipse, if not check [here] (<https://www.eclipse.org/community/eclipse_newsletter/2015/june/article3.php>)
  
  ![container run] (qe_screenshots/1.png)

  - Add the required Docker plugin related views in the Eclipse
  
  ![docker tooling views] (qe_screenshots/2.png)

  - After adding the views, go to Docker Explorer view and create new Docker connection

  ![new docker connection] (qe_screenshots/2_5.png)

  - Verify that `docker` daemon inside ADB box is not pingable without authentication

  ![failed ping] (qe_screenshots/3.png)

  - Enter the path to the certs as displayed by adbinfo output by `DOCKER_CERT_PATH` variable, hit `Test Connection`  and verify that ping successds. After ping succeeds, hit `Finish` button to create the connection `Docker Explorer` view.

  ![success ping] (qe_screenshots/4.png)

  - Once the `adb-eclipse` (names relative) connection is shown, exapand the view, right click on the `Images` icon and hit `Pull image` option, it will show up a view, enter the name of image you want to pull.
  
  ![image pull] (qe_screenshots/5.png)

- Image should be pulled inside the box and show up under the `Images` icon. Right click on the image and select `Run Image..` option. Lets create a container from the image we just pulled, and verify that container gets created and check the output from the container.

  ![pulled image] (qe_screenshots/6.png)
  
  ![container run view] (qe_screenshots/7.png)
  
  ![container run view] (qe_screenshots/8.png)

- Modify the the host port in Vagrantfile and reload the box `vagrant reload`, re-run the the plugin `vagrant adbinfo`, verify that modified host port is listed correctly in `DOCKER_HOST` variable.

```ruby
 config.vm.network "forwarded_port", guest: 2376, host: 5555, auto_correct: true
```

- SSH into the ADB vagrant box
   - check if the images pulled via Eclipse exist
   - pull any image inside the box `docker pull` and verify it appears in Eclipse under `Images` icon

- Try manually removing the certs directory `.vagrant/machines/default/virtualbox/.docker/` and re-run the plugin, it should copy the certs again.
