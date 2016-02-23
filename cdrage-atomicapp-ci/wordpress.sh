#!/bin/bash
echo "
##########
$1: TESTING WORDPRESS EXAMPLE
##########
"

docker build -t projectatomic/mariadb-centos7-atomicapp \
  -f nulecule-library/mariadb-centos7-atomicapp/Dockerfile \
  --no-cache \
  nulecule-library/mariadb-centos7-atomicapp/

docker build -t wordpress \
  -f nulecule-library/wordpress-centos7-atomicapp/Dockerfile \
  --no-cache \
  nulecule-library/wordpress-centos7-atomicapp/

run_wordpress() {
  echo "
[mariadb-atomicapp]
  db_user = foo
  db_pass = foo
  db_name = foo

[wordpress]
  db_user = foo
  db_pass = foo
  db_name = foo
  " >> answers.conf
  mkdir build
  atomic run wordpress --provider=$1 -a answers.conf -v --destination=build
}

stop_wordpress() {
  atomic stop wordpress --provider=$1 -v build/

  # Remove Docker-provider-specific containers
  if [[ $1 == "docker" ]]; then
    docker rm -f mariadb-atomicapp-app wordpress-atomicapp wordpress || true

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
  run_wordpress ${@:2}
elif [[ $1 == "stop" ]]; then
  stop_wordpress ${@:2}
else
  echo $"Usage: wordpress.sh {run|stop}"
  exit 1
fi
