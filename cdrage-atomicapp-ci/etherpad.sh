#!/bin/bash
echo "
##########
$1: TESTING ETHERPAD EXAMPLE
##########
"

docker build -t projectatomic/mariadb-centos7-atomicapp \
  -f nulecule-library/mariadb-centos7-atomicapp/Dockerfile \
  --no-cache \
  nulecule-library/mariadb-centos7-atomicapp/

docker build -t etherpad \
  -f nulecule-library/etherpad-centos7-atomicapp/Dockerfile \
  --no-cache \
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
  atomic run etherpad --provider=$1 -a answers.conf -v --destination=build
}

stop_etherpad() {
  atomic stop etherpad --provider=$1 -v build/

  # Remove Docker-provider-specific containers
  if [[ $1 == "docker" ]]; then
    docker rm -f mariadb-atomicapp-app etherpad-atomicapp etherpad || true

  # Wait for k8s containers to finish terminating
  # will change in the future to something in providers/kubernetes.sh
  elif [[ $1 == "kubernetes" ]]; then
    echo "Waiting for k8s po/svc/rc to finish terminating..."
    kubectl get po,svc,rc
    sleep 3 # give kubectl chance to catch up to api call
    while [ 1 ]
    do
      k8s=`kubectl get po,svc,rc | grep Terminating`
      if [[ $k8s == "" ]]
      then
        echo "k8s po/svc/rc terminated!"
        exit
      else
        echo "..."
      fi
      sleep 1
    done

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
