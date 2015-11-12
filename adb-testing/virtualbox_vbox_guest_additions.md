### CDK + Eclipse with vbox guest additions for VirtualBox provider

- `vagrant plugin install vagrant-vbguest`
- Use following Vagrantfile

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  
  config.vm.box = "atomicapp/dev"

  config.vm.network "forwarded_port", guest: 2376, host: 2379, auto_correct: true

  if !Vagrant.has_plugin?("vagrant-vbguest")
    puts "'vagrant-vbguest' plugin is required"
    puts "This can be installed by running:"
    puts
    puts " vagrant plugin install vagrant-vbguest"
    puts
    exit
  end


  config.vm.provision "shell", inline: <<-SHELL
    # =========================================================                                                                                             
    # Generate Certs for running TLS enabled docker daemon
    
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
  
  # setup the synced folders
  config.vm.synced_folder ".", "/home/vagrant/.docker/"
  config.vbguest.no_remote = true

end
```

 - Run `vagrant up`  this will install the vbox guest additions inside the guest, (be patient)
 - you should have the certs in your current directory
 - clients can make connection using `127.0.0.1:2379` and using the certs present in local directory
 - for testing with docker do (on host)

    ```
    cp -r *.pem  ~/.docker
    docker -H 127.0.0.1:2379 --tlsverify images
    ```
