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
[mariadb-atomicapp]
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
  # Workaround atomic cli bug prior to 1.8 so we must determine if the
  # version of atomic cli is at least 1.8. Do this by comparing the
  # atomic cli version with "1.8". If the lesser version is "1.8"
  # then the version we are using is >= "1.8".
  atomicversion=$(atomic --version)
  lesserversion=$(echo -e "${atomicversion}\n1.8" | sort -V | head -n 1)
  if [ "$lesserversion" != '1.8' ]; then
    atomicapp stop -v --logtype=nocolor build/
  else
    atomic stop etherpad -v --logtype=nocolor build/
  fi

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
