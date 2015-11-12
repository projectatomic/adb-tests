CDK + Eclipse with scp and ssh for VirtualBox provider
- `vagrant plugin install vagrant-triggers`
-  Export following into a `Vagrantfile`
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "atomicapp/dev"

  config.vm.network "forwarded_port", guest: 2376, host: 2379, auto_correct: true
    if !Vagrant.has_plugin?("vagrant-triggers")
      puts "'vagrant-triggers' plugin is required"
      puts "This can be installed by running:"
      puts
      puts " vagrant plugin install vagrant-triggers"
      puts
      exit
  end

  config.vm.provision "shell", inline: <<-SHELL
    # =========================================================                                                                                             
    # Generate Certs for running TLS enabled docker daemon
    #!/bin/bash
    
    # Todo: move the files into place
    
    # Generate Certificates to use with the docker daemon
    # Instructions sourced from http://docs.docker.com/articles/https/
    
    # Get the certificate location, i.e. setting the DOCKER_CERT_PATH variable
    . /etc/sysconfig/docker
    
    # randomString from http://utdream.org/post.cfm/bash-generate-a-random-string
    # modified to echo value
    
    function randomString {
            # if a param was passed, it's the length of the string we want
            if [[ -n $1 ]] && [[ "$1" -lt 20 ]]; then
                    local myStrLength=$1;
            else
                    # otherwise set to default
                    local myStrLength=8;
            fi
    
            local mySeedNumber=$$`date +%N`; # seed will be the pid + nanoseconds
            local myRandomString=$( echo $mySeedNumber | md5sum | md5sum );
            # create our actual random string
            #myRandomResult="${myRandomString:2:myStrLength}"
            echo "${myRandomString:2:myStrLength}"
    }
    
    # Get a temporary workspace
    dir=`mktemp -d`
    cd $dir
    
    # Get a random password for the CA and save it
    passfile=tmp.pass
    password=$(randomString 10)
    echo $password > $passfile
    
    # Generate the CA
    openssl genrsa -aes256 -passout file:$passfile -out ca-key.pem 2048
    openssl req -new -x509 -passin file:$passfile -days 365 -key ca-key.pem -sha256 -out ca.pem -subj "/C=/ST=/L=/O=/OU=/CN=example.com"
    
    # Generate Server Key and Sign it
    openssl genrsa -out server-key.pem 2048
    openssl req -subj "/CN=example.com" -new -key server-key.pem -out server.csr
    # Allow from 127.0.0.1
    extipfile=extfile.cnf
    echo subjectAltName = IP:127.0.0.1 > $extipfile
    openssl x509 -req -days 365 -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -passin file:$passfile -extfile $extipfile
    
    # Generate the Client Key and Sign it
    openssl genrsa -out key.pem 2048
    openssl req -subj '/CN=client' -new -key key.pem -out client.csr
    extfile=tmp.ext
    echo extendedKeyUsage = clientAuth > $extfile
    openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out cert.pem -extfile $extfile -passin file:$passfile
    
    # Clean up
    
    # set the cert path as configured in /etc/sysconfig/docker
    
    ## Move files into place
    mv ca.pem $DOCKER_CERT_PATH
    mv server-cert.pem $DOCKER_CERT_PATH
    mv server-key.pem $DOCKER_CERT_PATH
    
    # since the default user is vagrant and it can run docker without sudo
    CLIENT_SIDE_CERT_PATH=/home/vagrant/.docker
    
    mkdir -p $CLIENT_SIDE_CERT_PATH
    cp $DOCKER_CERT_PATH/ca.pem $CLIENT_SIDE_CERT_PATH
    mv cert.pem key.pem $CLIENT_SIDE_CERT_PATH
    
    chown vagrant:vagrant $CLIENT_SIDE_CERT_PATH
    
    chmod 0444 $CLIENT_SIDE_CERT_PATH/ca.pem
    chmod 0444 $CLIENT_SIDE_CERT_PATH/cert.pem
    chmod 0444 $CLIENT_SIDE_CERT_PATH/key.pem
    chown vagrant:vagrant $CLIENT_SIDE_CERT_PATH/ca.pem
    chown vagrant:vagrant $CLIENT_SIDE_CERT_PATH/cert.pem
    chown vagrant:vagrant $CLIENT_SIDE_CERT_PATH/key.pem
    
    chmod -v 0400 $DOCKER_CERT_PATH/ca.pem $DOCKER_CERT_PATH/server-cert.pem $DOCKER_CERT_PATH/server-key.pem
    
    ## Remove remaining files
    cd
    echo rm -rf $dir
    
    # ============= end of script for generating the certs for TLS enabled docker daemon===
 
    sed -i.back '/OPTIONS=*/c\OPTIONS="--selinux-enabled -H tcp://0.0.0.0:2376 -H unix:///var/run/docker.sock --tlscacert=/etc/docker/ca.pem --tlscert=/etc/docker/server-cert.pem --tlskey=/etc/docker/server-key.pem --tlsverify"' /etc/sysconfig/docker
    sudo systemctl restart docker
  SHELL

  # triggers
  config.trigger.after :provision do
    hport = `vagrant ssh-config`.split("\n  ").find{|e| e.start_with?("Port") }.split(" ")[1] 
    run "scp -r -P #{hport} -o StrictHostKeyChecking=no -i .vagrant/machines/default/virtualbox/private_key vagrant@127.0.0.1:/home/vagrant/.docker/* ."
  end

end
```
- Run `vagrant up --provider virtualbox` (in the same directory where Vagrantfile exist)
- Run `vagrant provision`
- You should have the certs in your current directory which is created (or updated) as part of above step
- To test the client connection to `docker` daemon inside CDK: In the Vagrantfile at line no: 7, we have mapped host port `2379` to `docker` daemon port (2376) inside CDK, which means that you can access the daemon at (host machine) 127.0.0.1:2379.
  Following is an example of connecting via `docker` CLI to daemon over TLS enabled TCP connection
  
  ```bash
  # copy the certs (generated above) to proper place where `docker` (by default) look up
  cp -r *.pem  ~/.docker
  docker -H 127.0.0.1:2379 --tlsverify images
  ```
  Note: On host machine, if you have port 2379 in use, vagrant will try to auto_correct it and assign a different port. You need to keep an eye on the corrected port while vagrant is brigning the machine up. Note that this vagrant `auto_correct` feature works as expected for Virtualbox provider but for libvirt provider it does not auto_correct and does not even fail!

- To test out the connection with Eclipse kindly check <https://www.eclipse.org/community/eclipse_newsletter/2015/june/article3.php> and this Video by Xavier Coulon <https://www.youtube.com/watch?v=RUgEgtLux8Q>. More Eclipse Docker Tooling documentations are at <<https://wiki.eclipse.org/Linux_Tools_Project/Docker_Tooling/User_Guide>>
