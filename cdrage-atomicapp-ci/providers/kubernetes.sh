#!/bin/bash

start_k8s() {
  # Note: takes some time for the http server to pop up :)
  # MINIMUM 15 seconds
  echo "
  ##########
  STARTING KUBERNETES
  ##########
  "
  docker run --net=host -d gcr.io/google_containers/etcd:2.0.9 /usr/local/bin/etcd --addr=127.0.0.1:4001 --bind-addr=0.0.0.0:4001 --data-dir=/var/etcd/data
  docker run --net=host -d -v /var/run/docker.sock:/var/run/docker.sock gcr.io/google_containers/hyperkube:v0.21.2 /hyperkube kubelet --api_servers=http://localhost:8080 --v=2 --address=0.0.0.0 --enable_server --hostname_override=127.0.0.1 --config=/etc/kubernetes/manifests
  docker run -d --net=host --privileged gcr.io/google_containers/hyperkube:v0.21.2 /hyperkube proxy --master=http://127.0.0.1:8080 --v=2
  until nc -z 127.0.0.1 8080;
  do
      echo ...
      sleep 1
  done
}

# Delete via image name google_containers
# Delete all containers started (names start with k8s_)
# Run twice in-case a container is replicated during that time

stop_k8s() {
  echo "
  ##########
  STOPPING KUBERNETES
  ##########
  "
   docker ps -a | grep 'gcr.io/google_containers' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true
   docker ps -a | grep 'k8s_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true
}

answers_k8s() {
  echo "
  ##########
  GENERATING KUBERNETES ANSWERS FILE
  ##########
  "
  echo "[general]
  provider = kubernetes
  namespace = foo" > answers.conf
}

case "$1" in
        start)
            start_k8s 
            ;;
        stop)
            stop_k8s 
            ;;
        answers)
            answers_k8s
            ;;
        *)
            echo $"Usage: kubernetes.sh {start|stop|answers}"
            exit 1
esac
