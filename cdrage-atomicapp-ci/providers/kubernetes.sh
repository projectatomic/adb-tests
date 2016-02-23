#!/bin/bash

start_k8s() {
  # Note: takes some time for the http server to pop up :)
  # MINIMUM 15 seconds
  echo "
  ##########
  STARTING KUBERNETES
  ##########
  "
  # Use alpha for now since this contains the new hyperkube format going forward
  K8S_VERSION=1.2.0-alpha.7
  docker run \
  --volume=/:/rootfs:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:rw \
  --volume=/var/lib/kubelet/:/var/lib/kubelet:rw \
  --volume=/var/run:/var/run:rw \
  --net=host \
  --pid=host \
  --privileged=true \
  -d \
  gcr.io/google_containers/hyperkube-amd64:v${K8S_VERSION} \
  /hyperkube kubelet \
      --containerized \
      --hostname-override="127.0.0.1" \
      --address="0.0.0.0" \
      --api-servers=http://localhost:8080 \
      --config=/etc/kubernetes/manifests \
      --cluster-dns=10.0.0.10 \
      --cluster-domain=cluster.local \
      --allow-privileged=true --v=2


  until nc -z 127.0.0.1 8080;
  do
      echo ...
      sleep 1
  done
}


stop_k8s() {
  echo "
  ##########
  STOPPING KUBERNETES
  ##########
  "
  # Delete via image name google_containers
  # Delete all containers started (names start with k8s_)
  # Run twice in-case a container is replicated during that time
  echo "\n-----Removing all k8s containers-----\n"
  for run in {0..2}
  do
    docker ps -a | grep 'k8s_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
    docker ps -a | grep 'gcr.io/google_containers/hyperkube-amd64' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
  done
}

answers_k8s() {
  echo "
  ##########
  GENERATING KUBERNETES ANSWERS FILE
  ##########
  "
  echo "[general]
  provider = kubernetes
  namespace = default" > answers.conf
}

if [[ $1 == "answers" ]]; then
  answers_k8s
elif [[ $1 == "start" ]]; then
  start_k8s
elif [[ $1 == "stop" ]]; then
  stop_k8s
else
  echo $"Usage: kubernetes.sh {answers|start|stop}"
fi
