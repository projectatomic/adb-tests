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

if [[ $1 == "answers" ]]; then
  answers_docker
elif [[ $1 == "stop" ]]; then
  stop_docker
else
  echo $"Usage: docker.sh {answers|stop}"
fi

