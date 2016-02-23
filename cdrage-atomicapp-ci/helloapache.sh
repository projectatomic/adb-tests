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

run_helloapache() {
  mkdir build
  atomic run projectatomic/helloapache --provider=$1 -a answers.conf -v --destination=build
}

stop_helloapache() {
  atomic stop projectatomic/helloapache --provider=$1 -v build/

  # Wait for k8s containers to finish terminating
  # will change in the future to something in providers/kubernetes.sh
  if [[ $1 == "kubernetes" ]]; then
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
  run_helloapache ${@:2}
elif [[ $1 == "stop" ]]; then
  stop_helloapache ${@:2}
else
  echo $"Usage: helloapache.sh {run|stop}"
  exit 1
fi
