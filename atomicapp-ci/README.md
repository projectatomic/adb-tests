#### Atomic App tests

Requirements:

  - Docker 1.9 or above
  - Python 2.7 and Pip

Current providers:

  - Docker
  - OpenShift Origin
  - Kubernetes

Tested:
  
  - projectatomic/helloapache
  - projectatomic/wordpress-centos7-atomicapp

Each provider (with the exception of Docker) is ran in a container. 

Both OpenShift and Kubernetes providers will remove themselves upon test completion.

To run all providers:
`make all`

Individual providers:
```
make clean-all install docker 
make clean-all install openshift
make clean-all install kubernetes
```

To run against a certain PR, pass the number of the PR to the make file, ex:
`make clean-all install docker ATOMICAPP_PR=480`
or
`make all ATOMICAPP_PR=480`

This will download the PR and build a container against it.
