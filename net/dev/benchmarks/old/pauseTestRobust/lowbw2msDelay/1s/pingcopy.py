#!usr/bin/python

#####################
#  channon@iit.edu  #
#####################

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, OVSKernelSwitch, RemoteController, Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel, info

####################
#  System Imports  #
####################

import sys
import time
import os
import subprocess


######################
#  helper functions  #
######################

# bash commands
PIDQ = "sudo pgrep -f mininet: > tmp/pidlist"
#old
#PAUSE  ="sudo pgrep -f mininet: | sudo awk  \'{system(\"sudo kill --signal SIGSTOP -\"$1)}' -"
#RESUME ="sudo pgrep -f mininet: | sudo awk  \'{system(\"sudo kill --signal SIGCONT -\"$1)}' -"
#new

pIDS=''

def pidList():
    global pIDS
    list = subprocess.call(PIDQ,shell=True)
    with open('tmp/pidlist', 'r') as ins:
        for line in ins:
            pIDS+= ('%s%s' %(' -',line.rstrip('\n')))  
    print (pIDS)

pidList()

NPAUSE = 'sudo kill --signal SIGSTOP%s'%pIDS
NRESUME ='sudo kill --signal SIGCONT%s'%pIDS

def pause():
    process = subprocess.call(NPAUSE, shell=True)
    time.sleep(0.2)
    process = subprocess.call(NRESUME, shell=True)
    time.sleep(0.01)

class DssTopo(Topo):
    "DSS custom topo"
    
    def build(self):
        
        ################
        #  start TOPO  #
        ################
        host1= self.addHost('host1')

        host2= self.addHost('host2')

        s1=self.addSwitch('switch1')
        
        self.addLink(host1, s1, 
                     bw=1, delay='2ms')
        self.addLink(host2, s1, 
                     bw=1, delay='2ms')

def test():
    topo = DssTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    
    with open("noPause.test","a") as myfile:
        for x in range(0,1000):
            st1 = net.pingPairFull()
            #print 'pausing'
            time.sleep(0.01)
            #pause()
            myfile.write( repr(st1[0][2][3]))
            myfile.write('\n')
            


    net.stop()    

if __name__ == '__main__':
   setLogLevel('info')
   test()
