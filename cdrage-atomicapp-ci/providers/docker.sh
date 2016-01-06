#!/bin/bash

answers_docker() {
  echo "
  ##########
  GENERATING DOCKER ANSWERS FILE
  ##########
  "

  echo "[general]
  provider = docker
  namespace = foobar" > answers.conf
}

# Removes all containers that have been started under the Docker namespace
stop_docker() {
  echo "
  ##########
  STOPPING DOCKER CONTAINERS
  ##########
  "
   docker ps -a | grep 'foobar_' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
}

case "$1" in
        answers)
            answers_docker
            ;;
        stop)
            stop_docker 
            ;;
        *)
            echo $"Usage: docker.sh {answers|stop}"
            exit 1
esac
