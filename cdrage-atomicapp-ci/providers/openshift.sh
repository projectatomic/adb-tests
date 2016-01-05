#!/bin/bash

start_openshift() {
  # Start up Dockerized version of OpenShift Origin
  # Note: takes some time for the http server to pop up :)

  docker rm -f origin
  docker run -d --name "origin" \
    --privileged --pid=host --net=host \
    -v /:/rootfs:ro -v /var/run:/var/run:rw -v /sys:/sys -v /var/lib/docker:/var/lib/docker:rw \
    -v /var/lib/origin/openshift.local.volumes:/var/lib/origin/openshift.local.volumes \
    openshift/origin start
}

stop_openshift() {
  docker rm -f origin
}

answers_openshift() {
  # Create a new project and give standard openshift user permission
  docker exec -it origin oc new-project foo
  docker exec -it origin oc policy add-role-to-user admin openshift -n foo

  # Retrieve the API key to use
  API_KEY=`curl -k -L -D - -u openshift:openshift -H 'X-CSRF-Token: 1' 'https://localhost:8443/oauth/authorize?response_type=token&client_id=openshift-challenging-client' 2>&1 | grep -oP "access_token=\K[^&]*"`
  echo $API_KEY

  echo "[general]
  provider = openshift
  providerapi = https://localhost:8443
  accesstoken = $API_KEY 
  namespace = foo" > answers.conf

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
