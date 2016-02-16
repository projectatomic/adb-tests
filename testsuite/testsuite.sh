#!/bin/bash

# todo: get input from command line
export vagrant_SHARING=${vagrant_SHARING:-true}
export vagrant_BOX_PATH=${vagrant_BOX_PATH:-""}
export vagrant_PLUGINS_DIR=${vagrant_PLUGINS_DIR:-""}
export vagrant_VAGRANTFILE_DIRS=${vagrant_VAGRANTFILE_DIRS:-""}
export vagrant_RHN_USERNAME=${vagrant_RHN_USERNAME:-""}
export vagrant_RHN_PASSWORD=${vagrant_RHN_PASSWORD:-""}
export vagrant_PROVIDER=${vagrant_PROVIDER:-""}
export HOST_PLATFORM=${HOST_PLATFORM:-""}

TSlog=$PWD/output

if [ "$HOST_PLATFORM" == "lin" ]; then
    SCL="scl enable sclo-vagrant1 --"
else
    SCL=""
fi

if [ "$vagrant_PROVIDER" == "" ]; then
    # set default virtualization provider
    if [ "$HOST_PLATFORM" == "lin" ]; then
        vagrant_PROVIDER="libvirt"
    else
        vagrant_PROVIDER="virtualbox"
    fi
fi



vagrant_vm_clenup () {
    # remove all cdk virtualbox machines
    for vm in `VBoxManage list vms| grep '"tmp.*default'|sed -e 's/.*"\(.*\)".*/\1/'`;
    do
        VBoxManage unregistervm --delete $vm
    done
}

vagrant_plugins_cleanup () {
    # uninstall plugins
    plugins=`$SCL vagrant plugin list|grep -v '^ '|grep -v 'No plugins installed.'|awk '{print $1}'`
    for plugin in $plugins;
    do
        $SCL vagrant plugin uninstall $plugin
    done
}

run_tests () {
    # run_tests <vagrant_PLUGINS_DIR>
    for d in $testdirs
    do
        cd $d
        logdir=$logroot/$d
        mkdir -p $logdir
        output=$logdir/output
        vagrant_PLUGINS_DIR=$1 $SCL ./runtest.sh &> $output
        grep -q 'Phases: .* good, 0 bad' $output
        if [ $? == 0 ]; then
            echo -e "PASS\t$d"
            echo -e "PASS\t$d" >> $TSlog
        else
            echo -e "FAIL\t$d"
            echo -e "FAIL\t$d" >> $TSlog
        fi
        # move journal
        journal=`grep 'JOURNAL XML' $output | grep -o '/.*'`
        test -f "$journal" && mv $journal $logdir
        journal=`grep 'JOURNAL TXT' $output | grep -o '/.*'`
        test -f "$journal" && mv $journal $logdir
        cd - > /dev/null
    done
}

###############################################################################

testdirs=`find . -name runtest.sh|sed -e 's#/runtest.sh##'`
#testdirs="./Components/vagrant/adbinfo-plugin/smoke"
> $TSlog

############################
# test with upstream plugins
############################

vagrant_plugins_cleanup
logroot=`mktemp -d`
echo "logdir with upstream plugins: $logroot"
echo "logdir with upstream plugins: $logroot" >> $TSlog

run_tests ""

# don't have local plugins, exit
[ "$vagrant_PLUGINS_DIR" != "" -a -d "$vagrant_PLUGINS_DIR" ] || exit

#########################
# test with local plugins
#########################

vagrant_plugins_cleanup
logroot=`mktemp -d`
echo "logdir with local plugins: $logroot"
echo -e "\nlogdir with local plugins: $logroot" >> $TSlog

run_tests $vagrant_PLUGINS_DIR
