#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2015  Praveen Kumar <kumarpraveen.nitdgp@gmail.com>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#


# Usage python vagrant_run.py [-h] [-t TIMES] PATH

import subprocess
import sys
import logging
import os
from argparse import ArgumentParser

# Enable Logging
logger = logging.getLogger("Log")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - \
                              %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

def run_vagrant(path, retry=3):
    try:
        proc = subprocess.Popen(['vagrant', 'up', '--provider', 'virtualbox'],
                bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                close_fds=True, preexec_fn=os.setsid, cwd=path)

    except OSError as err:
        logger.error(err)
    check_retry = 0
    for line in iter(proc.stdout.readline, b''):
        logger.info(line)
        if line.find('Warning: Connection timeout. Retrying...') != -1:
            check_retry = check_retry + 1
        if check_retry > retry:
            proc.kill()
            kill_vagrant()
            destroy_box(path)
            return 'fail'
    if proc.wait():
        proc.kill()
        kill_vagrant()
        destroy_box(path)
    else:
        destroy_box(path)

def kill_vagrant():
    try:
        pro = subprocess.check_output(['pidof', 'ruby-mri'])
        subprocess.call(['kill', '-9', pro.rstrip()])
    except subprocess.CalledProcessError as err:
        logger.error(err)
def destroy_box(path):
    try:
        subprocess.call(['vagrant', 'destroy', '-f'],
                        cwd=path)
    except subprocess.CalledProcessError as err:
        logger.error(err)

if __name__ == '__main__':
    parser = ArgumentParser(description='Regression testing for Vagrant(up/destroy)')
    parser.add_argument('path', metavar='p', type=str,
                        help='Absolute path of Vagrantfile')
    parser.add_argument('-t','--times', type=int, default=10,
                        help="Number of time you want to run (default=10)")
    args = parser.parse_args()
    failures = 0
    for r in range(args.times):
        failure = run_vagrant(args.path)
        if failure == 'fail':
            failures += 1
    logger.info("No of failure: %d", failures)
