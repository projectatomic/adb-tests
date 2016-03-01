#!/bin/bash
echo "
##########
$1: TESTING WORDPRESS EXAMPLE
##########
"

docker build -t projectatomic/mariadb-centos7-atomicapp \
  -f nulecule-library/mariadb-centos7-atomicapp/Dockerfile \
  nulecule-library/mariadb-centos7-atomicapp/

docker build -t wordpress \
  -f nulecule-library/wordpress-centos7-atomicapp/Dockerfile \
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
  # Workaround atomic cli bug prior to 1.8 so we must determine if the
  # version of atomic cli is at least 1.8. Do this by comparing the
  # atomic cli version with "1.8". If the lesser version is "1.8"
  # then the version we are using is >= "1.8".
  atomicversion=$(atomic --version)
  lesserversion=$(echo -e "${atomicversion}\n1.8" | sort -V | head -n 1)
  if [ "$lesserversion" != '1.8' ]; then
    atomicapp stop -v build/
  else
    atomic stop wordpress -v build/
  fi

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
        break
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
