#!/bin/bash
RELEASE="1.5"
LINK="https://github.com/projectatomic/atomic/archive/v1.5.tar.gz"

# Install according to github docs 
# https://github.com/projectatomic/atomic/tree/master/docs/install
install_atomic() {
  echo "
  ##########
  INSTALLING ATOMIC CLI
  ##########
  "
  wget $LINK -O atomic.tar.gz
  tar -xvf atomic.tar.gz
  cd atomic-$RELEASE
  if [ -f /etc/redhat-release ]; then
    yum install -y epel-release python-pip pylint go-md2man
    pip install -r requirements.txt
    PYLINT=true make install # ignore pesky pylint
  else # assuming this is debian/ubuntu instead :)
    apt-get install -y make git python-selinux go-md2man python-pip
    pip install pylint
    ln /usr/local/bin/pylint /usr/bin/pylint
    pip install -r requirements.txt
    PYLINT=true make install # ignore pesky pylint
  fi
  cd ..
  rm -rf atomic-$RELEASE atomic.tar.gz
}

case "$1" in
        install)
            install_atomic
            ;;
        *)
            echo $"Usage: atomic.sh {install}"
            exit 1
 
esac
