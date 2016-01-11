#!/bin/bash
echo "
##########
$1: TESTING WORDPRESS EXAMPLE
##########
"

# We build mariadb. as wordpress uses an aggregated database of mariadb
docker build -t projectatomic/mariadb-centos7-atomicapp \
  -f nulecule-library/mariadb-centos7-atomicapp/Dockerfile \
  --no-cache \
  nulecule-library/mariadb-centos7-atomicapp/

docker build -t wordpress \
  -f nulecule-library/wordpress-centos7-atomicapp/Dockerfile \
  --no-cache \
  nulecule-library/wordpress-centos7-atomicapp/

case "$1" in
        run)
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
            atomic run wordpress --provider=$2 -a answers.conf --destination=build
            ;;
        stop)
            atomic stop wordpress --provider=$2 build/

            # Since the names are hard-coded
            docker rm -f mariadb-atomicapp-app wordpress-atomicapp || true
            ;;
        *)
            echo $"Usage: helloapache.sh {run|stop}"
            exit 1
esac
