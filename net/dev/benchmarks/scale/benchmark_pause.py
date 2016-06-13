#!usr/bin/python

##############################
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, OVSKernelSwitch, RemoteController, Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel, info

import sys
import time
import os
import subprocess
import logging

# log = str(sys.argv[2])
# logging.basicConfig(filename=log,level=logging.DEBUG)

num_hosts = int(sys.argv[1])

NPAUSE  = ''
NRESUME = ''
pIDS = ''

def pidList(net):
    global pIDS
    for host in net.hosts :
        pIDS += ' %s' % host.pid
    for s in net.switches :
        pIDS+= ' %s' % s.pid
    for c in net.controllers:
        pIDS += ' %s' %c.pid
    # print ('pids subject to pause: %s'%pIDS)

def setupPause():
    global pIDS, NPAUSE, NRESUME
    NPAUSE  = 'sudo /home/vagrant/virtual/VirtualTimeKernel/test_virtual_time/freeze_all_procs -f -p %s'%pIDS
    NRESUME = 'sudo /home/vagrant/virtual/VirtualTimeKernel/test_virtual_time/freeze_all_procs -u -p %s'%pIDS

def pause ():
    before_time = time.time()
    process = subprocess.call(NPAUSE,shell=True)
    after_time = time.time()
    # logging.info('pause,%s'% (after_time-before_time))

def resume ():
    before_time = time.time()
    process = subprocess.call(NRESUME,shell=True)
    after_time = time.time()
    # logging.info('resume,%s'% (after_time-before_time))

NPAUSE  = ''
NRESUME = ''

class DssTopo(Topo):
    "DSS custom topo"

    def build(self, topoConfig='default.config'):
        global num_hosts

        for i in range(num_hosts):
            host=self.addHost('H%s'%i)
            
          
def test(num):
    for i in range(0, num):
        time.sleep(0.1)
        pause()
        time.sleep(0.1)
        resume()
  
def start():
    topo = DssTopo()
    net = Mininet(topo, link = TCLink)
    net.start()
    pidList(net)
    setupPause()
    #call loop
    test(100)
    net.stop()

start()


