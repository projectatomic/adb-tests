#!/bin/bash

provider=$1

cat << EOF > answers.conf
[general]
namespace = default
provider = $provider

[redismaster-app]
image = jasonbrooks/redis
hostport = 6379

[redisslave-app]
image = jasonbrooks/redis
master_hostport = 6379
hostport = 6379
EOF

ret=0

echo "Running projectatomic/redis-centos7-atomicapp"
atomic run projectatomic/redis-centos7-atomicapp
res=$?
if [ $res -gt $ret ]; then
    ret=$res
fi

if [ $ret -eq 0 ]; then
    if [ "$provider" = "docker" ]; then
        total=0
        docker ps | egrep "redis-master" | egrep -q " Up "
        while [ $? -ne 0 -a $total -lt 120 ]; do
            sleep 2
            total=$((total+2))
            docker ps | egrep "redis-master" | egrep -q " Up "
        done
        sleep 2

        echo "Checking docker containers"
        docker ps

        docker ps | egrep "redis-master" | egrep -q " Up "
        res=$?
        if [ $res -gt $ret ]; then
            ret=$res
        fi

        host="0.0.0.0"
        port=`docker ps | egrep "redis-master" | sed -e "s/.*0.0.0.0://" -e "s/->.*//"`
    elif [ "$provider" = "kubernetes" ]; then
        total=0
        kubectl get pods | egrep -q "^redis-master-.*\s+Running\s+"
        while [ $? -ne 0 -a $total -lt 120 ]; do
            sleep 2
            total=$((total+2))
            kubectl get pods | egrep -q "^redis-master-.*\s+Running\s+"
        done

        echo "Checking kubernetes pod"
        kubectl get pods

        echo "Checking kubernetes services"
        kubectl get services

        kubectl get pods | egrep -q "^redis-master-.*\s+Running\s+"
        res=$?
        if [ $res -gt $ret ]; then
            ret=$res
        fi
        host=`kubectl get services | egrep "^redis-master" | awk '{print $(NF-1)}'`
        port=`kubectl get services | egrep "^redis-master" | awk '{print $NF}' | sed -e 's%/TCP%%'`

    fi

    times=0
    redis-cli -h $host -p $port ping
    while [ $? -ne 0 -a $times -lt 3 ]; do
        times=$((times+1))
        redis-cli -h $host -p $port ping
    done

    echo "Checking connectivity to master"
    redis-cli -h $host -p $port get key
    res=$?
    if [ $res -gt $ret ]; then
        ret=$res
    fi
fi

echo "Stopping projectatomic/redis-centos7-atomicapp"
atomic stop projectatomic/redis-centos7-atomicapp
res=$?
if [ $res -gt $ret ]; then
    ret=$res
fi

if [ "$provider" = "docker" ]; then
    docker stop redis-master redis-slave
    docker rm redis-master redis-slave
fi

exit $ret
