#!/bin/python

import subprocess
import time

PIDQ = "sudo pgrep -f mininet: > pidlist"
p=''

def pidList():
    global p
    list = subprocess.call(PIDQ,shell=True)
    with open('pidlist', 'r') as ins:
        for line in ins:
            p+= ('%s%s' %(' -',line.rstrip('\n')))  
    print (p)

pidList()

PAUSE = 'sudo kill --signal SIGSTOP%s'%p
RESUME ='sudo kill --signal SIGCONT%s'%p

def test():
    while 1:
        process = subprocess.call(PAUSE, shell=True)
        time.sleep(0.3)
        process = subprocess.call(RESUME, shell=True)
        time.sleep(0.3)

test()
