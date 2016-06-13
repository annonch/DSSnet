#!/bin/python

import subprocess

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

def Ptest():
    process = subprocess.call(PAUSE, shell=True)
    
def Rtest():
    process = subprocess.call(RESUME, shell=True)


