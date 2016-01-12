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
            atomic run etherpad --provider=$2 -a answers.conf --destination=build
            ;;
        stop)
            atomic stop etherpad --provider=$2 build/

            # Since the names are hard-coded
            docker rm -f mariadb-atomicapp-app etherpad-atomicapp || true
            ;;
        *)
            echo $"Usage: etherpad.sh {run|stop}"
            exit 1
esac
