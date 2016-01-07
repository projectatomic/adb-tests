TestCases To Test ADB Vagrant Box

####ADB box should boot fine through Vagrant.
* vagrant up -> vagrant ssh should work fine

####Docker service should be running at the boot of the vagrant box
* check `sudo systemctl status docker`

####ADB Vagrant box should have the docker storage setup.
* `sudo lvs` output should look like as below
```{r}
[vagrant@localhost ~]$ sudo lvs
  LV          VG    Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  docker-pool vg001 twi-a-t--- 12.66g             0.15   0.10                            
  root        vg001 -wi-ao----  8.00g 
```
####docker pull and run should run
* `docker pull centos` should download the docker centos docker image
* `docker run -i -t centos /bin/bash` should run the docker container and give the input prompt to the container
 

####Single node k8s setup should be in place in the Vagrant box
*This testcase will change after next ADB release*
* `kubectl get nodes` command should give below result.
```
$ kubectl get nodes
NAME        LABELS                             STATUS
127.0.0.1   kubernetes.io/hostname=127.0.0.1   Ready
```

####We should be able to run helloapache atomicapp 
*This testcase will change after next ADB release*
* Refer https://hub.docker.com/r/projectatomic/helloapache/

####To test vagrant sanity (up/destroy)
* Execute vagrant_run script (Use -h option to check available options)
