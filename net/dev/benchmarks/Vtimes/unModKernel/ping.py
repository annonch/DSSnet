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
PIDQ = "pgrep -f mininet: > tmp/pidlist"

pIDS=''
linkOps=dict(bw=10)#,delay='0')
numOfSwitches = int(sys.argv[1])
FileOut= sys.argv[2]
stime= float(sys.argv[4])

def pidList(net):
    global pIDS
    for host in net.hosts :
        pIDS += ' %s' % host.pid
    for s in net.switches :
        pIDS += ' %s' % s.pid
    for c in net.controllers:
        pIDS += ' %s' %c.pid
    print (pIDS)

NPAUSE=''
NRESUME=''

def pause():
    print NPAUSE
    process = subprocess.call(NPAUSE, shell=True)
    time.sleep(stime)
    print NRESUME
    process = subprocess.call(NRESUME, shell=True)
    #time.sleep(0.1)

class DssTopo(Topo):
    "DSS custom topo"
    
    def build(self):
        
        ################
        #  start TOPO  #
        ################
        host1= self.addHost('h1')
        host2= self.addHost('h2')

        switchList=[]
        for i in range(numOfSwitches):

            s=self.addSwitch('switch%s'%i)
            switchList.append(s)
            if len(switchList) == 1 :
                self.addLink(host1, s, **linkOps)
            else :
                self.addLink(switchList[len(switchList)-2],s,**linkOps)
        self.addLink(host2,switchList[len(switchList)-1] , **linkOps)

def test():
    topo = DssTopo()
    net = Mininet(topo, link=TCLink)
    net.start()

    pidList(net)

    global NPAUSE
    global NRESUME

    NPAUSE = 'sudo /home/vagrant/vTime/VirtualTimeKernel/test_virtual_time/freeze_all_procs -f -p %s'%pIDS
    NRESUME ='sudo /home/vagrant/vTime/VirtualTimeKernel/test_virtual_time/freeze_all_procs -u -p %s'%pIDS
    
    #block
    print(net.get('h1').cmd('ping -c 1 10.0.0.2'))

    net.get('h1').cmd('~/cosim/cosim/mininet/benchmarks/ping_mod/VirtualTimeKernel/iputils/ping -c 1000 10.0.0.2 > %sbl.test 2>&1 '% FileOut)
    '''
    #dont block
    net.get('h1').cmd('ping -A -c 1000 10.0.0.2 > %svt.test 2>&1 &'% FileOut)
    for x in range(0,int(sys.argv[3])):
        print 'pausing'
        pause()
        time.sleep(stime)
	print 'resumed'
    '''
    CLI(net)
    net.stop()    

if __name__ == '__main__':
   setLogLevel('info')
   test()
