#!/bin/bash
echo "
##########
$1: TESTING ETHERPAD EXAMPLE
##########
"

# Build mariadb - etherpad uses mariadb
docker build -t projectatomic/mariadb-centos7-atomicapp \
  -f nulecule-library/mariadb-centos7-atomicapp/Dockerfile \
  nulecule-library/mariadb-centos7-atomicapp/

# Build etherpad
docker build -t etherpad \
  -f nulecule-library/etherpad-centos7-atomicapp/Dockerfile \
  nulecule-library/etherpad-centos7-atomicapp/


run_etherpad() {
  echo "
[mariadb-centos7-atomicapp:mariadb-atomicapp]
  db_user = foo
  db_pass = foo
  db_name = foo

[etherpad-app]
  db_user = foo
  db_pass = foo
  db_name = foo
  " >> answers.conf
  mkdir build
  atomic run etherpad --provider=$1 \
    -a answers.conf -v --destination=build --logtype=nocolor
}

stop_etherpad() {
  atomic stop etherpad -v --logtype=nocolor build/

  # Remove Docker-provider-specific containers
  if [[ $1 == "docker" ]]; then
    docker rm -f mariadb-atomicapp-app etherpad-atomicapp etherpad || true
  elif [[ $1 == "kubernetes" ]]; then
    ./providers/kubernetes.sh wait
  elif [[ $1 == "openshift" ]]; then
    ./providers/openshift.sh wait
  fi
}

if [[ $1 == "run" ]]; then
  run_etherpad ${@:2}
elif [[ $1 == "stop" ]]; then
  stop_etherpad ${@:2}
else
  echo $"Usage: etherpad.sh {run|stop}"
  exit 1
fi
