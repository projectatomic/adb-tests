### Current flow


- `job.yaml` contains the Jenkins Job Builder configuration which we push to
  CentOS CI using `jenkins-jobs update job.yaml`.

- Above command will set environment variables on slave system.

- It also uploads the `run.py` file to CentOS CI and loads it in the
  "Execute Python script" section of the configuration. This script gets
  executed on the slave and asks
  [Duffy](https://wiki.centos.org/QaWiki/CI/Duffy) for a node to execute tests
  on.

- Currently the script gets executed only when someone triggers a job manually.
  However, this needs to be automated. Maybe nightly?

- Once Duffy provides a system for testing, `run.py` installs git and ansible
  on it. Then the ansible playbook in *placeholder*
  [ci-ansible](https://github.com/dharmit/ci-ansible) repo gets executed on the
  system which installs required packages on the system.

- Ansible playbooks need to be moved to a proper place. However, they cannot be
  written on per-test basis either since many tests will require installing
  same packages. [Ansible
  tags](http://docs.ansible.com/ansible/playbooks_tags.html) can be used
  instead.

- Post playbook execution, we clone the
  [adb-tests](https://github.com/dharmit/adb-tests) repo and execute the tests.

**NOTE: This flow needs to be discussed and improved. This is just a POC and
far from ideal.**
