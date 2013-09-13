#!/usr/local/env python
import subprocess

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

subprocess.Popen('killall -v mongod', shell=True, executable='/bin/bash')
subprocess.Popen('mongod --fork', shell=True, executable='/bin/bash')
subprocess.Popen('uwsgi --ini ./uwsgi.ini', shell=True, executable='/bin/bash')

print \
    FAIL + '---------------------------------\n' + ENDC +\
    FAIL + 'SUMMARY:#########################\n' + ENDC +\
    WARNING + '\n1) mongod started in fork mode\n' +\
                '2) uwsgi started\n' + ENDC +\
    FAIL + '\n---------------------------------' +\
    ENDC
