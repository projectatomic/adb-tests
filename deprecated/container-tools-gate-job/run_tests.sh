#!/bin/bash

source functions.sh $*

install_packages

job_rtn=0;

for provider in $providers; do
    configure $provider

    startup $provider

    for test in $tests; do
        rtn_code=$?
    
        if [ $rtn_code -eq 0 ]; then
            chmod u+x ./$test
            ./$test $provider
            rtn_code=$?
        fi
    
        if [ $rtn_code -eq 0 ]; then
            echo "+++++ $test ($provider) passed +++++"
        else
            echo "+++++ $test ($provider) failed +++++"
        fi
    
        if [ $job_rtn -eq 0 ]; then
            job_rtn=$rtn_code
        fi
    
        cleanup $provider
    done

    shutdown $provider
done
exit $job_rtn
