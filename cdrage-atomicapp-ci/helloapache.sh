#!/bin/bash
echo "
##########
$1: TESTING HELLOAPACHE EXAMPLE
##########
"
mkdir build

docker build -t projectatomic/helloapache \
  -f nulecule-library/helloapache/Dockerfile \
  nulecule-library/helloapache

atomic run projectatomic/helloapache --provider=$1 -a answers.conf --destination=build
