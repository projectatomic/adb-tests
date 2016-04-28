#!/usr/bin/python

import subprocess
import unittest
import re
import os
from unittest import TestCase

regex_for_vagrantfile = re.compile(
    "components/centos/centos-openshift-setup/Vagrantfile"
)


def is_openshift_custom_vagrantfile_modified():
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


class OpenShiftTests(TestCase):
    """This class tests Openshift on ADB box."""

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
                cwd='/root/adb/components/centos/centos-openshift-setup'
            )
        except:
            pass
        self.assertEqual(exit_code, 0)

    def test_03_VagrantDestroy(self):
        """Check force destroy vagrant box."""
        try:
            exit_code = subprocess.check_call(
                ['vagrant', 'destroy', '-f'],
                cwd="/root/adb/components/centos/"
                "centos-openshift-setup"
            )
        except:
            pass
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    configure_git()
    if is_openshift_custom_vagrantfile_modified():
        unittest.main()
