#!/bin/bash

start_openshift() {
  # Start up Dockerized version of OpenShift Origin
  # Note: takes some time for the http server to pop up :)
  # MINIMUM 15 seconds
  echo "
  ##########
  STARTING OPENSHIFT 
  ##########
  "
  docker rm -f origin
  docker run -d --name "origin" \
    --privileged --pid=host --net=host \
    -v /:/rootfs:ro -v /var/run:/var/run:rw -v /sys:/sys -v /var/lib/docker:/var/lib/docker:rw \
    -v /var/lib/origin/openshift.local.volumes:/var/lib/origin/openshift.local.volumes \
    openshift/origin start
  until nc -z 127.0.0.1 8443;
  do
      echo ...
      sleep 1
  done
}

stop_openshift() {
  echo "
  ##########
  STOPPING OPENSHIFT 
  ##########
  "
  docker rm -f origin

  # Remove underlying kubernetes containers created as result of using OpenShift with k8s as back-end
  docker ps -a | grep 'gcr.io/google_containers' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true
  docker ps -a | grep 'k8s_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f || true
}

answers_openshift() {
  echo "
  ##########
  GENERATING OPENSHIFT ANSWERS FILE
  ##########
  "

  # Retrieve the API key to use
  API_KEY=`curl -k -L -D - -u openshift:openshift -H 'X-CSRF-Token: 1' 'https://localhost:8443/oauth/authorize?response_type=token&client_id=openshift-challenging-client' 2>&1 | grep -oP "access_token=\K[^&]*"`
  echo $API_KEY

  docker exec -it origin oc config set-credentials openshift --token=$API_KEY
  docker exec -it origin oc config set-cluster openshift1 --server=https://localhost:8443 --insecure-skip-tls-verify=true
  docker exec -it origin oc config set-context openshift --cluster=openshift1 --user=openshift
  docker exec -it origin oc config use-context openshift
  docker exec -it origin oc config set contexts.openshift.namespace foo
  docker exec -it origin oc new-project foo

  echo "[general]
  provider = openshift
  providerapi = https://localhost:8443
  accesstoken = $API_KEY 
  namespace = foo
  providertlsverify = False" > answers.conf

  echo "OpenShift Origin answers file located at $PWD"
}

case "$1" in
        start)
            start_openshift
            ;;
        stop)
            stop_openshift
            ;;
        answers)
            answers_openshift
            ;;
        *)
            echo $"Usage: openshift.sh {start|stop|answers}"
            exit 1
esac
