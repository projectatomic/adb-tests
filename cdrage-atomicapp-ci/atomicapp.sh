#!/bin/bash

# TO CHANGE, temporary:
LINK="https://github.com/projectatomic/atomicapp"
UPSTREAM="projectatomic/atomicapp"

install_atomicapp() {
  echo "
  ##########
  INSTALLING ATOMICAPP CLI
  ##########
  "
  git clone $LINK
  cd atomicapp

  if [ "$1" ]
    then
      echo "USING PR: $1"
      BRANCH_NAME=`curl -s "https://api.github.com/repos/${UPSTREAM}/pulls/${1}" | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["head"]["ref"]'`
      USERS_NAME=`curl -s "https://api.github.com/repos/${UPSTREAM}/pulls/${1}" | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["head"]["user"]["login"]'`
      echo "User's name: " $USERS_NAME
      echo "Pull-request: " $1
      echo "Pull-request branch name: " $BRANCH_NAME
      git checkout -b $1-$USERS_NAME-$BRANCH_NAME
      curl -s "https://patch-diff.githubusercontent.com/raw/${UPSTREAM}/pull/${1}.patch" | git am
  fi

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
            install_atomicapp $2
            ;;
        docker)
            docker_atomicapp
            ;;
        *)
            echo $"Usage: atomicpp.sh {install|docker}"
            exit 1
 
esac
