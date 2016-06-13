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
import shlex


log = str(sys.argv[2])
logging.basicConfig(filename=log,level=logging.DEBUG)

num_hosts = int(sys.argv[1])

pIDS = ''

fh=0 

def pidList(net):
    global pIDS
    for host in net.hosts :
        pIDS += ' %s' % host.pid
    for s in net.switches :
        pIDS+= ' %s' % s.pid
    for c in net.controllers:
        pIDS += ' %s' %c.pid
    #print ('pids subject to pause: %s'%pIDS)
NPAUSE  = ''
NRESUME = ''

def setupPause():
    global pIDS, NPAUSE, NRESUME, fh
    NPAUSE  = 'sudo /home/vagrant/virtual/VirtualTimeKernel/test_virtual_time/freeze_all_procs -f -p %s\n'%pIDS
    #print(len(NPAUSE))
    NRESUME = 'sudo /home/vagrant/virtual/VirtualTimeKernel/test_virtual_time/freeze_all_procs -u -p %s\n'%pIDS
    
    pro = 'sudo /home/vagrant/virtual/VirtualTimeKernel/test_virtual_time/freeze_listen %s '%pIDS
    #print(pro)
    
    args = shlex.split(pro)

    subprocess.Popen(args)


filename = '/tmp/fifo.tmp'
    
fh = open(filename,"w",0)


def pause ():

    global fh

    before_time = time.time()
    #process = subprocess.call(NPAUSE,shell=True)
    #//fh.write((NPAUSE))
    fh.write('p')
    after_time = time.time()
    logging.info('pause,%s'% (after_time-before_time))
    
    #fh.close()


def resume ():
    global fh
    #filename = 'fifo.tmp'
    
    #fh = open(filename,"w")
    

    before_time = time.time()
    #process = subprocess.call(NRESUME,shell=True)
    #fh.write((NRESUME))
    fh.write('u')
    after_time = time.time()
    logging.info('resume,%s'% (after_time-before_time))
    #fh.close()
    

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
        time.sleep(0.3)
        pause()
        time.sleep(0.3)
        resume()
  
def start():
    topo = DssTopo()
    net = Mininet(topo, link = TCLink)
    net.start()
    pidList(net)
    setupPause()
    #call loop
    test(100)


start()
