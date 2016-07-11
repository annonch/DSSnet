#!usr/bin/python

##########################
#  channon@hawk.iit.edu  #
##########################

# DSSnet
# version 2.0

#####################
#  Mininet Imports  #
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
import zmq
import logging
import argparse
import thread
import heapq
import shlex

# local

import models.pipe
import DSSnet_handler as handler
import DSSnet_hosts
import DSSnet_events

######################
#  Global Variables  #
###################### 

COORD_PIPE = 'tmp/coordination.pipe'
if not os.path.exists(COORD_PIPE):
    os.mkfifo(COORD_PIPE)

# parser

parser = argparse.ArgumentParser(description= 'Manages network emulation and synchronizes with the power Coordinator.')
parser.add_argument('--version', action='version', version='DSSnet 2.0')
parser.add_argument('--ip', help='ip of power coordinator', default='10.47.142.26', type=str)
parser.add_argument('--port', help='port of the power coordinator, default/recommended: 50021', default='50021', type=str)
parser.add_argument('--topo_config', help='path to topology file',default='./configs/topo.config', type=str)
parser.add_argument('--IED_config', help='path to IED file', default='./configs/IED.config',type=str)
parser.add_argument('--sync_event_log', help='path to logging file for synchronization events', default='logs/synch_event.log', type=str)
#parser.add_argument('--window_size', help='maximum synchonization time(ms) for blocking events. see docs for more info', default = 0, type=int)
parser.add_argument('-c','--c','--clean', action='store_const' , const = 1, help='cleans DSSnet, should be ran before running DSSnet')

args = parser.parse_args()
    
logging.basicConfig(filename=args.sync_event_log,level=logging.DEBUG)

# open transport layer to power coordinator
# TCP socket

contextOutDSS=zmq.Context()
DSSout=contextOutDSS.socket(zmq.REQ)

print 'Opening Connection to tcp://%s:%s' % (args.ip,args.port)
DSSout.connect('tcp://%s:%s' % (args.ip,args.port))

# Virtual time helpers

pIDS=' '

def pidList(net):
    global pIDS
    for host in net.hosts:
        pIDS += ' %s' % host.pid
    for s in net.switches:
        pIDS += ' %s' % s.pid
    for c in net.controllers:
        pIDS += ' %s' % c.pid
    print ('pids in virtual time: %s' % pIDS)


def setupPause():
    global pIDS, fh
    #open listener
    pross = 'sudo /home/vagrant/virtual/VirtualTimeKernel/test_virtual_time/freeze_listen %s' % pIDS
    argss = shlex.split(pross)
    subprocess.Popen(argss)
    
    filename = '/tmp/fifo.tmp'
    fh=open(filename,"w",0)
#
#  Interface to virtual time
#
    
def pause ():
    fh.write('p')
    before_time = time.time()
    logging.info('pause time: %s'%before_time)
    
def resume ():
    fh.write('u')
    before_time = time.time()
    logging.info('resume time: %s'%time.time())    

#event Queue

eventQueue = []

# main event loop
#  waiting for sync event

num_block = 0 # used to determine if multiple blocking events are recieved before pausing can occur in order not to repeat the block

com_lock=thread.allocate_lock()

def pipe_listen (net):
    pipein = open(COORD_PIPE, 'r')
    global startTime
    global num_block
    global eventQueue
    heapq.heapify(eventQueue)

    # start sync thread
    thread.start_new_thread(sync,())
    
    while True:
        newEvent = pipein.readline()[:-1] # trim newline character
        print newEvent
        # if event has arrived
        if newEvent:
            event = newEvent.split()
            if event[1] == 'b': # blocking
                num_block+=1
                pause()

            
            # add event to priority queue
            heapq.heappush(eventQueue,
                           DSSnet_events.Events(newEvent,event[5]))
            
                        
            # sync new thread
            # thread.start_new_thread(sync,newEvent)
            
def sync():
    global eventQueue
    global num_block
    global net
    global hosts
    while 1:
        try:
            e_obj = heapq.heappop(eventQueue)
            newEvent = e_obj.get_event() 
            event = newEvent.split()
            logging.info('event being processed: %s' % event)
            try:
                preprocess=getattr(handler,event[3])
                processed_event=preprocess(newEvent,net,hosts)
            except AttributeError:
                print('pre-process error: %s' % newEvent)
                logging.info('pre-process error with event request %s' % newEvent)
        
            with com_lock: # mutual exclusivity is required with com (shouldnt be a problem)
                reply = do_com(processed_event)

            thread.start_new_thread(postProcess,(reply,newEvent))
    
        except (IndexError, AttributeError):
            # no event in Queue
            pass
    
def postProcess(reply,newEvent):
    global net,hosts,num_block,pipes
    event = newEvent.split()
    try:
        postprocess=getattr(handler,event[4])
        processed_event=postprocess(newEvent,reply,net,hosts,pipes)
    except AttributeError:
        print('post process error:  %s' % newEvent)
        logging.info('post process error with event request: %s' % newEvent)

    #models.pipe.send_sync('hi',pipes['h1'])
    
    if event[1] == 'b':
        num_block -= 1
        if num_block == 0:
            resume()
    thread.exit()

    
def do_com(request):
    req_bytes=request.encode('utf-8')
    DSSout.send(req_bytes)
    status=DSSout.recv()
    data = status.decode('utf-8')
    logging.info('reply recieved %s: ' % data)
    return data

hosts = []

class topo(Topo):
    "creates topology"

    def build(self):
        
        global hosts

        with open(args.IED_config, 'r') as ins:
            for line in ins:
                if line[0] != '#': # comment
                    # expecting a dssnet_host object format
                    properties = line.split(' split ') # wont interfere with command 
                    # msg id command
                    hosts.append(DSSnet_hosts.DSSnet_hosts(properties[1], properties[0], properties[3], properties[2]))
                    host = self.addHost(properties[0])

        with open(args.topo_config, 'r') as ins:
            for line in ins:
                if line[0] != '#':
                    
                    elements = line.split()
                    if elements[0] == 'new' :
                        self.addSwitch(elements[1])
                    else:
                        self.addLink(elements[0],elements[1])#,elements[2])

pipes={}
                
def setup_pipes(net):
    global hosts

    for i in hosts:

        fn = './tmp/%s' % i.get_host_name()

        print 'creating pipe: %s '%fn

        if not os.path.exists(fn):
            os.mkfifo(fn)
        pipes[i.get_host_name()] = os.open(fn,os.O_WRONLY)



def run_main():
    global hosts
    global net
    
    top = topo()
    net = Mininet(top, link = TCLink)
    net.start()

    # set IP
    for i in hosts:
        net.get(i.get_host_name()).cmd('ifconfig %s-etho %s' % (i.get_host_name, i.get_ip))
    
    print('Dumping Host Connections')
    dumpNodeConnections(net.hosts)

    pidList(net)
    setupPause()
    time.sleep(1)

    # start commands
    for i in hosts:
        print i.get_process_command()
        net.get(i.get_host_name()).cmd(i.get_process_command())
        
    setup_pipes(net)

    global startTime
    startTime = time.time()
    print('initiation finished')
    if os.fork():
        pipe_listen(net)
    CLI(net)


if __name__ == '__main__':
    
    setLogLevel('info')
    if args.c:
        subprocess.Popen('./clean.sh')
        exit()
    run_main()

# fin
