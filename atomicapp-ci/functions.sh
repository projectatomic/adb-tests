#!/bin/bash

docker_services="etcd docker"
kubernetes_services="kube-proxy kubelet kube-scheduler kube-controller-manager kube-apiserver $docker_services"

providers="docker"
tests="hello_apache.sh"

function parse_opts {
    local OPTIND opt p
    while getopts "p:t:" opt; do
        case $opt in
        p)
            providers=`echo $OPTARG | tr ',' ' '`
            ;;
        t)
            tests=`echo $OPTARG | tr ',' ' '`
            ;;
        esac
   done

   shift $((OPTIND - 1))
}

function configure() {
    local prov=$1
    if [ "$prov" = "docker" ]; then
        :
    elif [ "$prov" = "kubernetes" ]; then
        key_dir="/etc/pki/kube-apiserver"
        key_file="$key_dir/serviceaccount.key"
        mkdir -p $key_dir
        /bin/openssl genrsa -out $key_file 2048
        sed -i -e "s%KUBE_API_ARGS=\".*\"%KUBE_API_ARGS=\"--service_account_key_file=$key_file\"%" /etc/kubernetes/apiserver
        sed -i -e "s%KUBE_CONTROLLER_MANAGER_ARGS=\".*\"%KUBE_CONTROLLER_MANAGER_ARGS=\"--service_account_private_key_file=$key_file\"%" /etc/kubernetes/controller-manager

        fix_kubernetes_issue_29
    else
        echo "Unknown provider '$prov'"
        exit 1 
    fi
}

function get_services() {
    local prov=$1
    if [ "$prov" = "docker" ]; then
        echo "$docker_services"
    elif [ "$prov" = "kubernetes" ]; then
        echo "$kubernetes_services"
    else
        echo "Unknown provider '$prov'"
        exit 1 
    fi
}

function startup() {
    local prov=$1
    shutdown $prov
    start_services $(get_services $prov)
}

function cleanup() {
    local prov=$1
    if [ "$prov" = "docker" ]; then
        if [ `docker ps -aq | wc -l` -gt 0 ]; then
            docker rm $(docker ps -aq)
        fi
        if [ `docker images -aq | wc -l` -gt 0 ]; then
            docker rmi $(docker images -aq)
        fi
    fi
    rm -rf .workdir Dockerfile Nulecule answers.conf artifacts
}

function shutdown() {
    local prov=$1
    cleanup $prov
    stop_services $(get_services $prov)
}

function start_services() {
    local services=$*
    rtn_code=0
    for s in $services; do
        service $s start
        if [ $? -gt $rtn_code ]; then
            rtn_code=$?
        fi
    done

    sleep 5
    return $rtn_code
}

function stop_services() {
    local services=$*
    for s in `echo $services | awk '{ for (i=NF; i>0; --i) printf("%s%s", $i, (i>1?OFS:ORS))}'`; do
        service $s stop
    done
    return 0
}

function fix_kubernetes_issue_29 {
    # Fixing issue #29
    cat << EOF > /etc/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
EnvironmentFile=-/etc/kubernetes/config
EnvironmentFile=-/etc/kubernetes/apiserver
User=kube
ExecStart=/usr/bin/kube-apiserver \\
            \$KUBE_LOGTOSTDERR \\
            \$KUBE_LOG_LEVEL \\
            \$KUBE_ETCD_SERVERS \\
            \$KUBE_API_ADDRESS \\
            \$KUBE_API_PORT \\
            \$KUBELET_PORT \\
            \$KUBE_ALLOW_PRIV \\
            \$KUBE_SERVICE_ADDRESSES \\
            \$KUBE_ADMISSION_CONTROL \\
            \$KUBE_API_ARGS
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
}

parse_opts $*

function install_packages() {

    echo 'Yum updating the host'
    yum -y -d0 upgrade

    echo 'Installing atomic'
    yum -y -d 1 install atomic kubernetes etcd flannel mariadb redis

    rpm -qa | egrep -q '^redis'
    if [ $? -ne 0 ]; then
        back=`pwd`
        echo 'Installing redis'
        mkdir /tmp/redis.$$
        cd /tmp/redis.$$
        yum -y -d 1  install wget   
        wget -r --no-parent -A 'epel-release-*.rpm' http://dl.fedoraproject.org/pub/epel/7/x86_64/e/
        rpm -Uvh dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-*.rpm
        yum -y -d 1  install redis   
        cd $back
    fi

    echo 'Patching atomic stop.'
    yum -y -d 1 install patch
    patch -N -p 0 -u /usr/lib/python2.7/site-packages/Atomic/atomic.py < 2748df6.patch
}
