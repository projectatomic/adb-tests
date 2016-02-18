#!/bin/bash
echo "
##########
$1: TESTING HELLOAPACHE EXAMPLE
##########
"

docker build -t projectatomic/helloapache \
  -f nulecule-library/helloapache/Dockerfile \
  --no-cache \
  nulecule-library/helloapache

case "$1" in
        run)
            mkdir build
            atomic run projectatomic/helloapache --provider=$2 -a answers.conf -v --destination=build
            ;;
        stop)
            atomic stop projectatomic/helloapache --provider=$2 -v build/
            ;;
        *)
            echo $"Usage: helloapache.sh {run|stop}"
            exit 1
esac
