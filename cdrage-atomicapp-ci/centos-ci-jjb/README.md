# Atomic App CentOS CI JJB Information

This directory contains the files needed to update the Atomic App
CI jobs within the CentOS CI. The following steps illustrate how
to update the jobs.

You must first install the `jenkins-jobs` executable on your machine:

```
# dnf install /usr/bin/jenkins-jobs
    or
# yum install /usr/bin/jenkins-jobs
```

Next create a file that will hold the username/password of the user
you are connecting to the CentOS CI instance as:

```
# cat <<EOF > jenkins_jobs.ini
[jenkins]
user=username
password=password
url=https://ci.centos.org
EOF
```

Edit the files to make whatever changes that are needed to the jobs.
The `run.py` file contains the python script that will execute on
jenkins slaves. The `project.yaml` file holds the jjb yaml (which will
import the `run.py` file).

After you have made your edits you can call `jenkins-jobs` to update
the jobs. It should look something like this:

```
# jenkins-jobs --conf jenkins_jobs.ini update project.yaml
INFO:root:Updating jobs in ['project.yaml'] ([])
WARNING:jenkins_jobs.local_yaml:tag '!include-raw' is deprecated, switch to using '!include-raw:'
INFO:jenkins_jobs.local_yaml:Including file './run.py' from path '.'
INFO:jenkins_jobs.builder:Number of jobs generated:  6
INFO:jenkins_jobs.builder:Reconfiguring jenkins job atomicapp-test-docker-master
INFO:jenkins_jobs.builder:Reconfiguring jenkins job atomicapp-test-docker-pr
INFO:jenkins_jobs.builder:Reconfiguring jenkins job atomicapp-test-kubernetes-master
INFO:jenkins_jobs.builder:Reconfiguring jenkins job atomicapp-test-kubernetes-pr
INFO:jenkins_jobs.builder:Reconfiguring jenkins job atomicapp-test-openshift-master
INFO:jenkins_jobs.builder:Reconfiguring jenkins job atomicapp-test-openshift-pr
INFO:root:Number of jobs updated: 6
INFO:jenkins_jobs.builder:Cache saved
```
