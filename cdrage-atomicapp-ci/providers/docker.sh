#!/bin/bash

answers_docker() {
  echo "[general]
  provider = docker
  namespace = foo" > answers.conf
}

case "$1" in
        answers)
            answers_docker
            ;;
        *)
            echo $"Usage: docker.sh {answers}"
            exit 1
esac
