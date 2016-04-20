#!/usr/bin/python

import subprocess
import unittest
import re
import os
from unittest import TestCase

ANSIBLE_REPO = "https://github.com/dharmit/ci-ansible"

regex_for_vagrantfile = re.compile(
    "components/centos/centos-k8s-singlenode-setup/Vagrantfile"
)


def is_k8s_custom_vagrantfile_modified():
    """Check if any custom vagrantfile is modified."""
    modified_files = git_diff_tree()

    for _ in modified_files:
        if regex_for_vagrantfile.match(_):
            return True
        else:
            continue
    return False


def git_diff_tree():
    """Return a list of files that got modified in the PR."""
    files = subprocess.check_output(['git', 'diff-tree', '--no-commit-id',
                                     '--name-only', '-r', "%s" %
                                     (os.environ['ghprbActualCommit'])],
                                    cwd="/root/adb")
    return files.split("\n")


def configure_git():
    # To be able to checkout the PR branch
    subprocess.check_call(
        ["git",
         "config",
         "--add",
         "remote.origin.fetch",
         "+refs/pull/*/head:refs/remotes/origin/pr/*"
         ],
        cwd="/root/adb"
    )

    # Fetch all branches (including PRs)
    subprocess.check_call(
        ["git", "fetch", "origin"],
        cwd="/root/adb"
    )

    # Checkout the PR
    subprocess.check_call(
        ["git", "checkout", "pr/%s" % os.environ["ghprbPullId"]],
        cwd="/root/adb"
    )


class KubernetesTests(TestCase):

    """This class tests Kubernetes on ADB box."""

    def test_01_service_manager_install(self):
        """Install required plugins."""
        # vagrant-service-manager plugin is required to boot up ADB box
        subprocess.check_call(
            ['vagrant', 'plugin', 'install', 'vagrant-service-manager']
        )

    def test_02_VagrantUp(self):
        """Check if vagrant up succeeds."""
        try:
            # ADB repo is cloned to /root/adb using Ansible
            exit_code = subprocess.check_call(
                ['vagrant', 'up'],
                cwd='/root/adb/components/centos/centos-k8s-singlenode-setup'
            )
        except:
            pass
        self.assertEqual(exit_code, 0)

    def test_03_kubectl_output(self):
        """Check if k8s is properly setup."""
        # Dirty hack to ensure below check doesn't fail due to service taking
        # time to start
        subprocess.call(["sleep", "5"])
        try:
            output = subprocess.check_output(
                ['vagrant', 'ssh', '-c', '%s' % "kubectl get nodes"],
                cwd="/root/adb/components/centos/centos-k8s-singlenode-setup"
            )
        except:
            pass
        self.assertIn('127.0.0.1', output.split())
        self.assertIn('Ready', output.split())

    def test_04_atomic_app(self):
        """Check if atomicapp starts properly."""
        try:
            subprocess.call([
                "vagrant", "ssh", "-c", "%s" %
                "sudo yum -y install epel-release && "
                "sudo yum -y install ansible"
            ])
            subprocess.call([
                "vagrant", "ssh", "-c", "%s" %
                "git clone %s " % ANSIBLE_REPO
            ])
            subprocess.call([
                "vagrant", "ssh", "-c", "%s" %
                "cd ci-ansible && ansible-playbook install-atomicapp.yaml"
            ])
            subprocess.call([
                "vagrant", "ssh", "-c", "%s" %
                "atomic run projectatomic/helloapache"
            ])

            # This sleep gives time to atomicapp to start the app on k8s
            subprocess.call(["sleep", "60"])
            output = subprocess.check_output([
                "vagrant", "ssh", "-c", "%s" %
                "kubectl get pods| grep helloapache"
            ])
            self.assertIn("helloapache", output)
            self.assertIn("Running", output)

        except:
            pass

    def test_05_VagrantDestroy(self):
        """Check force destroy vagrant box."""
        try:
            exit_code = subprocess.check_call(
                ['vagrant', 'destroy', '-f'],
                cwd="/root/adb/components/centos/"
                "centos-k8s-singlenode-setup"
            )
        except:
            pass
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    configure_git()
    if is_k8s_custom_vagrantfile_modified():
        unittest.main()
