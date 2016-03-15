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
  # Workaround atomic cli bug prior to 1.8 so we must determine if the
  # version of atomic cli is at least 1.8. Do this by comparing the
  # atomic cli version with "1.8". If the lesser version is "1.8"
  # then the version we are using is >= "1.8".
  atomicversion=$(atomic --version)
  lesserversion=$(echo -e "${atomicversion}\n1.8" | sort -V | head -n 1)
  if [ "$lesserversion" != '1.8' ]; then
    atomicapp stop -v build/
  else
    atomic stop projectatomic/helloapache -v build/
  fi

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
