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
            atomic run wordpress --provider=$2 -a answers.conf -v --destination=build
            ;;
        stop)
            atomic stop wordpress --provider=$2 -v build/

            # Remove Docker-provider-specific containers
            docker rm -f mariadb-atomicapp-app wordpress-atomicapp || true

            # Sometimes mariadb takes *forever* to shut-down (don't know why) via k8s. Force remove it.
            docker ps -a | grep 'k8s_mariadb' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true

            ;;
        *)
            echo $"Usage: wordpress.sh {run|stop}"
            exit 1
esac
