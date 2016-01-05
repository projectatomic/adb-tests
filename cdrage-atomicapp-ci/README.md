#### Atomic App tests

Requirements:

  - Docker 1.8 or above
  - Python 2.7 and Pip

Current providers:

  - Docker
  - OpenShift Origin
  - Kubernetes

Tested:
  
  - projectatomic/helloapache
  - projectatomic/wordpress-centos7-atomicapp

Each provider (with the exception of Docker) is ran in a container. 

OpenShift will remove itself after it has been tested, however, __Kubernetes__ will not due to the multiple redundant Docker containers created.

To run all providers:
`make all`

Individual providers:
```
make clean-all
make install
make openshift


make clean-all
make install
make kubernetes
```
