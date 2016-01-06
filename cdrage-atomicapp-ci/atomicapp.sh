#!/bin/bash

# TO CHANGE, temporary:
LINK="https://github.com/projectatomic/atomicapp"

install_atomicapp() {
  echo "
  ##########
  INSTALLING ATOMICAPP CLI
  ##########
  "
  git clone $LINK
  cd atomicapp
  make install
  cd ..
  rm -rf atomicapp
}

# Builds the atomicapp image as atomicapp:build
docker_atomicapp() {
  echo "
  ##########
  BUILDING ATOMICAPP CONTAINER
  ##########
  "
	docker pull centos:7
  git clone $LINK
  cd atomicapp
  docker build -t atomicapp:build .
  cd ..
  rm -rf atomicapp
}

case "$1" in
        install)
            install_atomicapp
            ;;
        docker)
            docker_atomicapp
            ;;
        *)
            echo $"Usage: atomicpp.sh {install|docker}"
            exit 1
 
esac

