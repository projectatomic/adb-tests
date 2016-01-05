#!/bin/bash

start_k8s() {
  docker run --net=host -d gcr.io/google_containers/etcd:2.0.9 /usr/local/bin/etcd --addr=127.0.0.1:4001 --bind-addr=0.0.0.0:4001 --data-dir=/var/etcd/data

  docker run --net=host -d -v /var/run/docker.sock:/var/run/docker.sock gcr.io/google_containers/hyperkube:v0.21.2 /hyperkube kubelet --api_servers=http://localhost:8080 --v=2 --address=0.0.0.0 --enable_server --hostname_override=127.0.0.1 --config=/etc/kubernetes/manifests

  docker run -d --net=host --privileged gcr.io/google_containers/hyperkube:v0.21.2 /hyperkube proxy --master=http://127.0.0.1:8080 --v=2
}

answers_k8s() {
  echo "[general]
  provider = kubernetes
  namespace = foo" > answers.conf
}

case "$1" in
        start)
            start_k8s 
            ;;
        answers)
            answers_k8s
            ;;
        *)
            echo $"Usage: kubernetes.sh {start|answers}"
            exit 1
esac
