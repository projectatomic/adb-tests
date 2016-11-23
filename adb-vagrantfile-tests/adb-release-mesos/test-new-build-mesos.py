#!/usr/bin/python

import os
import sys
import unittest
import subprocess

from unittest import TestCase

VAGRANTFILE_PATH = \
    "/root/adb/components/centos/centos-mesos-marathon-singlenode-setup/" \
    "Vagrantfile"

CWD = "/root/adb/components/centos/centos-mesos-marathon-singlenode-setup/"


class MesosTests(TestCase):

    """This class tests for Mesos provider on ADB box"""

    def test_01_pull_Vagrant_box(self):
        try:
            exit_code = subprocess.check_call(
                ['vagrant', 'box', 'add', '--name', 'adb-latest',
                 '%s' % os.environ['libvirtbox']]
            )
        except:
            sys.exit(1)
        self.assertEqual(exit_code, 0)

    def test_02_VagrantUp(self):
        try:
            # Vagrantfile would boot projectatomic/adb. We need to modify this
            # to use the latest box (adb-latest) that's supposed to be
            # released. Hence using sed
            with open(VAGRANTFILE_PATH) as f:
                filedata = f.read()

            newdata = filedata.replace("projectatomic/adb", "adb-latest")

            with open(VAGRANTFILE_PATH, "w") as f:
                f.write(newdata)

            exit_code = subprocess.check_call(
                ['vagrant', 'up'],
                cwd=CWD
            )
        except:
            sys.exit(1)
        self.assertEqual(exit_code, 0)

    def test_03_check_services_status(self):
        services = {
            "zookeeper": "",
            "marathon": "",
            "mesos-master": "",
            "mesos-slave": ""
        }
        for s in services:
            try:
                cmd = "systemctl is-active %s" % s
                out = subprocess.check_output(
                    ['vagrant', 'ssh', '-c', '%s' % cmd],
                    cwd=CWD
                    )
                services[s] = out.strip()
            except:
                pass
        for s in services:
            self.assertEqual(services[s], 'active')

    def test_04_start_atomicapp(self):
        setup_atomicapp = "sudo yum -y install atomicapp"

        start_helloapache = \
            "sudo atomicapp run --provider=marathon projectatomic/helloapache"

        api_request = \
            "curl localhost:8080/v2/apps/helloapache"
        try:
            subprocess.check_call(
                ['vagrant', 'ssh', '-c', '%s' % setup_atomicapp],
                cwd=CWD
            )
            subprocess.check_call(
                ['vagrant', 'ssh', '-c', '%s' % start_helloapache],
                cwd=CWD
            )

            out = subprocess.check_output(
                ['vagrant', 'ssh', '-c', '%s' % api_request],
                cwd=CWD
            )

        except:
            pass

        self.assertIn('"appId":"/helloapache"', out)

    def test_05_VagrantDestroy(self):
        """Check force destroy vagrant box."""
        try:
            exit_code = subprocess.check_call(
                ['vagrant', 'destroy', '-f'],
                cwd=CWD
            )
        except:
            pass
        self.assertEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()
