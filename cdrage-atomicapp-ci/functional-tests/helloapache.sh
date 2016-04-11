#!/bin/bash
echo "
##########
$1: TESTING HELLOAPACHE EXAMPLE
##########
"

docker build -t projectatomic/helloapache \
  -f nulecule-library/helloapache/Dockerfile \
  nulecule-library/helloapache

run_helloapache() {
  mkdir build
  atomic run projectatomic/helloapache --provider=$1 \
    -a answers.conf -v --destination=build --logtype=nocolor
}

stop_helloapache() {
  atomic stop projectatomic/helloapache -v --logtype=nocolor build/

  # Wait for k8s/oc containers to finish terminating
  if [[ $1 == "kubernetes" ]]; then
    ./providers/kubernetes.sh wait
  elif [[ $1 == "openshift" ]]; then
    ./providers/openshift.sh wait
  fi
}

if [[ $1 == "run" ]]; then
  run_helloapache ${@:2}
elif [[ $1 == "stop" ]]; then
  stop_helloapache ${@:2}
else
  echo $"Usage: helloapache.sh {run|stop}"
  exit 1
fi
