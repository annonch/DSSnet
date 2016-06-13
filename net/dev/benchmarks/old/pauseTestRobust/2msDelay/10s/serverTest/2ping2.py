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
        s2=self.addSwitch('switch2')
        s3=self.addSwitch('switch3')
        s4=self.addSwitch('switch4')
        s5=self.addSwitch('switch5')
        s6=self.addSwitch('switch6')
        s7=self.addSwitch('switch7')
        s8=self.addSwitch('switch8')
        s9=self.addSwitch('switch9')
        s10=self.addSwitch('switch10')





        self.addLink(host1, s1, 
                     bw=10, delay='2ms')
        self.addLink(s1,s2,bw=10, delay='2ms')
        self.addLink(s2,s3,bw=10, delay='2ms')
        self.addLink(s3,s4,bw=10, delay='2ms')
        self.addLink(s4,s5,bw=10, delay='2ms')
        self.addLink(s5,s6,bw=10, delay='2ms')
        self.addLink(s6,s7,bw=10, delay='2ms')
        self.addLink(s7,s8,bw=10, delay='2ms')
        self.addLink(s8,s9,bw=10, delay='2ms')
        self.addLink(s9,s10,bw=10, delay='2ms')

        self.addLink(host2, s10, 
                     bw=10, delay='2ms')

def test():
    topo = DssTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    '''    
    with open("pause.test","a") as myfile:
        for x in range(0,2000):
            st1 = net.pingPairFull()
            #print 'pausing'
            time.sleep(0.01)
            pause()
            myfile.write( repr(st1[0][2][3]))
            myfile.write('\n')

    with open("noPause.test","a") as myffile:
        for x in range(0,2000):
            st1 = net.pingPairFull()
            #print 'pausing'
            time.sleep(0.01)
            #pause()
            myffile.write( repr(st1[0][2][3]))
            myffile.write('\n')

    '''     
    CLI(net)        


    net.stop()    

if __name__ == '__main__':
   setLogLevel('info')
   test()
