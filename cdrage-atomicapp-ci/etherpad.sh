#!/bin/bash
echo "
##########
$1: TESTING ETHERPAD EXAMPLE
##########
"

docker build -t etherpad \
  -f nulecule-library/etherpad-centos7-atomicapp/Dockerfile \
  --no-cache \
  nulecule-library/etherpad-centos7-atomicapp/

case "$1" in
        run)
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
            atomic run etherpad --provider=$2 -a answers.conf -v --destination=build
            ;;
        stop)
            atomic stop etherpad --provider=$2 -v build/

            # Remove Docker-provider-specific containers
            docker rm -f mariadb-atomicapp-app etherpad-atomicapp etherpad || true

            # Sometimes mariadb takes *forever* to shut-down (don't know why) via k8s. Force remove it.
            docker ps -a | grep 'k8s_mariadb' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true
            ;;
        *)
            echo $"Usage: etherpad.sh {run|stop}"
            exit 1
esac
