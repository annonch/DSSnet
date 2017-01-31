#!/usr/bin/python

##########################
#  channon@hawk.iit.edu  #
##########################

# DSSnet
# version 2.0

#####################
#  Mininet Imports  #
##################### 

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, OVSKernelSwitch, RemoteController, Host, OVSBridge
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections, quietRun, specialClass
from mininet.log import setLogLevel, info, warn, error, debug
from mininet.nodelib import LinuxBridge
from mininet.examples.controlnet import MininetFacade


####################
#  System Imports  #
####################

import sys
import time
import os
from os import environ
from os.path import dirname,join, isfile
from glob import glob
from functools import partial
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
import onos

######################
#  Global Variables  #
###################### 

COORD_PIPE = 'tmp/coordination.pipe'
if not os.path.exists(COORD_PIPE):
    os.mkfifo(COORD_PIPE)
# parser

parser = argparse.ArgumentParser(description= 'Manages network emulation and synchronizes with the power Coordinator.')
parser.add_argument('--version', action='version', version='DSSnet 2.0')
parser.add_argument('-ip','--ip', help='ip of power coordinator', default='10.47.142.26', type=str)
parser.add_argument('-port','--port', help='port of the power coordinator, default/recommended: 50021', default='50021', type=str)
parser.add_argument('-topo','--topo_config', help='path to topology file',default='./configs/topo.config', type=str)
parser.add_argument('-IED','--IED_config', help='path to IED file', default='./configs/IED.config',type=str)
parser.add_argument('-sel','--sync_event_log', help='path to logging file for synchronization events', default='logs/synch_event.log', type=str)
#parser.add_argument('--window_size', help='maximum synchonization time(ms) for blocking events. see docs for more info', default = 0, type=int)
parser.add_argument('-c','--c','--clean', action='store_const' , const = 1, help='cleans DSSnet, should be ran before running DSSnet')
parser.add_argument('-onos','--onos', action='store_const', const=1, help='use onos (default yes)')
parser.add_argument('-nc','--numControllers', help='number of controllers for onos to use',default=3,type=int)
parser.add_argument('-tm','--test_mode',help='test mode for debugging',default=0,type=int)
parser.add_argument('-mpt',help='WARNING DO NOT CHANGE',default=0.05,type=float)
parser.add_argument('-pause', help='enable use of pause',dest = 'pause',action='store_false')
parser.add_argument('-logLevel','-ll',help = 'logging level: info warn error debug',default='info',type=str)
parser.add_argument('-stp',help = 'use stp protocol on switches',dest = 'stp',action='store_true')
parser.add_argument('-rstp',help = 'use rstp protocol on switches',dest = 'rstp',action='store_true')
parser.add_argument('-ovs_pid_files',help='path to dir containing ovsdb-server.pid and ovs-vswitchd.pid',default='/usr/local/var/run/openvswitch/',type=str)
parser.add_argument('-ovs_vt',help='enabling this flag removes ovs from vt', default = 'store_true', action='store_false',dest = 'ovs_vt')
parser.add_argument('-tdf', help='time dilation factor',default = 1,type=int)
parser.add_argument('-kern',help='kernel switch or user switch, default kernel',dest = 'kern',action='store_false',default='store_true')
args = parser.parse_args()

setLogLevel('info')

    
logging.basicConfig(filename=args.sync_event_log,level=logging.WARNING)

if args.kern:
    print('kernel switch used')
else:
    print('user switch detected')

if args.stp and args.onos:
    warn("stp and onos enabled")

if args.stp and args.onos:
    warn("rstp and onos enabled")

if args.stp and args.rstp:
    error("stp and rstp can not both be enabled")
    exit(1)

if args.stp:
    print('stp enabled')

elif args.rstp:
    print('rstp enabled')

elif args.onos:
    print('onos enabled')

else:
    print('custom controller')

if args.ovs_vt:
    print('ovs in virtual time')
else:
    print('ovs not in virtual time')

MIN_PAUSE_INTERVAL = args.mpt


# open transport layer to power coordinator
# TCP socket

contextOutDSS=zmq.Context()
DSSout=contextOutDSS.socket(zmq.REQ)

print 'Opening Connection to tcp://%s:%s' % (args.ip,args.port)
DSSout.connect('tcp://%s:%s' % (args.ip,args.port))

debug=1

# Virtual time helpers

pIDS=' '
ovsdb_pid = ' '
vswitchd_pid = ' '

def ovs_dilate():
    global pIDS, ovsdb_pid, vswitchd_pid
    
    filename= '%sovsdb-server.pid' % args.ovs_pid_files
    
    with open(filename, 'r') as ins:
      fdata = [line.rstrip() for line in ins]
      ovsdb_pid = fdata[0]
      pIDS += ' %s' % fdata[0]
      
    filename= '%sovs-vswitchd.pid' % args.ovs_pid_files
    with open(filename, 'r') as ins:
        fdata = [line.rstrip() for line in ins]
        vswitchd_pid = fdata[0]
        pIDS += ' %s' %fdata[0]

    cmd_str = 'dilate_all_procs -t %d -p %s %s ' % (args.tdf * 1000, vswitchd_pid, ovsdb_pid)
    subprocess.check_output(cmd_str, shell=True)
  
def ovs_restore():
    global ovsdb_pid, vswitchd_pid
    filename= '%sovsdb-server.pid' % args.ovs_pid_files
    print (filename)
    with open(filename, 'r') as ins:
        fdata = [line.rstrip() for line in ins]
        ovsdb_pid = fdata[0]

    filename= '%sovs-vswitchd.pid' % args.ovs_pid_files
    with open(filename, 'r') as ins:
        fdata = [line.rstrip() for line in ins]
        vswitchd_pid = fdata[0]
    
    cmd_str = 'dilate_all_procs -t %d -p %s %s ' % (args.tdf * 0, vswitchd_pid, ovsdb_pid)
    print cmd_str
    subprocess.check_output(cmd_str, shell=True)

def pidList(net):
    global pIDS
    for host in net.hosts:
        pIDS += ' %s' % host.pid
    for s in net.switches:
        pIDS += ' %s' % s.pid
    for c in net.controllers:
        pIDS += ' %s' % c.pid
    #find pids of onos controllers
    if args.onos:
        for h in controlNetwork.net.hosts:
            pIDS += ' %s' % h.pid
        for s in controlNetwork.net.switches:
            pIDS += ' %s' % s.pid
        #for c in controlNetwork.net.controllers:
        #    #pIDS += ' %s' % c.pid


    print ('pids in virtual time: %s' % pIDS)

#
#  Interface to virtual time
#
    
def pause ():
    global net,controlNetwork
    if args.pause:
        net.freezeEmulation()
        if args.onos:
            controlNetwork.net.freezeEmulation()
        if args.ovs_vt:
            cmd_str= 'freeze_all_procs -p %s %s -f' % (ovsdb_pid ,vswitchd_pid)
            subprocess.check_output(cmd_str, shell=True)
        if debug:
            before_time = time.time()
            if args.test_mode >2:
                print('pause time: %s'%before_time)
            logging.info('pause time: %s'%before_time)

def resume_ovs(): 
    cmd_str= 'freeze_all_procs -p %s %s -u' % (ovsdb_pid ,vswitchd_pid)
    subprocess.check_output(cmd_str, shell=True)


def resume ():
    global net
    if args.pause:
        net.freezeEmulation('unfreeze')
        if args.onos:
            controlNetwork.net.freezeEmulation('unfreeze')
        if args.ovs_vt:
            resume_ovs()
        time.sleep(MIN_PAUSE_INTERVAL)

        if debug:
            before_time = time.time()
            if args.test_mode >2:
                print('resume time: %s'%before_time)
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
                if num_block < 1:
                    pause()
                num_block+=1
                
            
            # add event to priority queue
            heapq.heappush(eventQueue,
                           DSSnet_events.Events(newEvent,event[5]))
            
previous_time = -10.0 # some inconsistencies at the ms level
            
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(beginning_of_time = -10.0) # just use arbitrary negative value
def adjust_time(event):
    global previous_time
    old_GToD = event[5]
    if adjust_time.beginning_of_time < 0.0:
        adjust_time.beginning_of_time = float(event[5])
        event[5] = str(0.00001)# very small because 0 breaks things 
    else:
        new_time = float(event[5]) - float(adjust_time.beginning_of_time)
        if new_time < previous_time:
            event[5] = str(previous_time)
        else:
            event[5] = str(new_time)
    previous_time = float(event[5])
    #debugging virtual time
    if args.test_mode > 2:
        print('wall clock GToD: %s VT GToD: %s adjusted time: %s beginning of time %s'%(time.time(),old_GToD,event[5],adjust_time.beginning_of_time))
    
    logging.debug('wall clock GToD: %s VT GToD: %s adjusted time: %s beginning of time %s'%(time.time(),old_GToD,event[5],adjust_time.beginning_of_time))
    
    return event




'''
sync pulls an event from the event heap 
it runs the preprocessing function (user defined)
and sends the event to the power coordinator (if required)
lastly it creates a new thread to handle the post processing

rinse and repeat
'''


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
            #adjust time
            event = adjust_time(event)
            
            logging.warning('event beginning %f' % time.time())
            logging.info('event being processed: %s' % event)
            

            if event[2] == 'n':
                print 'test'
                x = net.configLinkStatus('s1','s2','down')
                print 'test finished?'
            try:
                preprocess=getattr(handler,event[3])
                processed_event=preprocess(event,net,hosts)
            except AttributeError:
                print('pre-process error: %s' % newEvent)
                logging.info('pre-process error with event request %s' % newEvent)
            
            # check destination of event (power or network)
            # if power sent to power coord.
            if event[2] == 'p':             
                with com_lock: # mutual exclusivity is required with com (shouldnt be a problem)
                    reply = do_com(processed_event)
            
            if event[2] == 'n':
                if args.test_mode > 1:
                    print('network event detected in DSSnet %s ' % newEvent)
                reply = processed_event

            if args.test_mode >2:
                print (reply)
            thread.start_new_thread(postProcess,(reply,newEvent))
            
        except (IndexError, AttributeError):
            # no event in Queue
            pass

'''

Post processing will run the post process handler 
 it also manages the resume interface if active blocking events
Then it dies :(

'''
    
def postProcess(reply,newEvent):
    global net,hosts,num_block,pipes
    event = newEvent.split()
    try:
        postprocess=getattr(handler,event[4])
        processed_event=postprocess(newEvent,reply,net,hosts,pipes)
    except AttributeError:
        print('post process error:  %s' % newEvent)
        logging.info('post process error with event request: %s' % newEvent)

    if event[1] == 'b':
        num_block -= 1
        if num_block == 0:
            resume()
    logging.warning('finish time: %f'%time.time())
    thread.exit()

    
''' 

do_com just sends the event to the power coordinator

'''

def do_com(req):
    #request is a list turn to string
    request = ' '.join(req)
    req_bytes=request.encode('utf-8')
    DSSout.send(req_bytes)
    status=DSSout.recv()
    data = status.decode('utf-8')
    logging.info('reply recieved %s: ' % data)
    return data

hosts = []

'''

This class reasds the IED configuration from file (user defined)
creates the network topology

'''

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
                    try:
                        hosts.append(DSSnet_hosts.DSSnet_hosts(properties[1], properties[0], properties[3], properties[2],properties[4]))
                        thost = self.addHost(properties[0])
                    except IndexError:
                        print 'no pipe info given'
                        hosts.append(DSSnet_hosts.DSSnet_hosts(properties[1], properties[0], properties[3], properties[2]))
                        thost = self.addHost(properties[0])
                    
        with open(args.topo_config, 'r') as ins:
            for line in ins:
                if line[0] != '#':
                    
                    elements = line.split()
                    if elements[0] == 'new' :
                        if args.stp:
                            self.addSwitch(elements[1],failMode='standalone',stp=1)
                        elif args.rstp:
                            self.addSwitch(elements[1],failMode='standalone',rstp=1)
                        else:
                            if args.kern:
                                self.addSwitch(elements[1])
                            else:
                                self.addSwitch(elements[1],switch='user')
                    else:
                        self.addLink(elements[0],elements[1])#,elements[2])

pipes={}
                
'''

setup pipes reads creates a pipe to each host so that the 

'''

def setup_pipes(net):
    global host
    global pipes

    for i in hosts:
        if i.pipe:
            fn = './tmp/%s' % i.get_host_name()
            print 'creating pipe: %s '%fn
            if not os.path.exists(fn):
                os.mkfifo(fn)
            pipes[i.get_host_name()] = os.open(fn,os.O_WRONLY)


#################### EXPeriment ################

def link_up_down(i,s1,s2):
    if i:
        print('%s %s down')
        net.configLinkStatus(s1, s2, 'down')
    else:
        print('%s %s up')
        net.configLinkStatus(s1, s2, 'up')
        
def pause_unpause(interval,inc,s1,s2):
    count=30

    while 1:
        count+=inc
        if count % 60 == 0 :
            if count % 120 == 0:
                link_up_down(0,s1,s2)
            else:
                link_up_down(1,s1,s2)

        time.sleep(interval)
        if args.test_mode >= 3:
            pause()
        time.sleep(interval)
        if args.test_mode >= 3:
            resume()

def custom_ping(interval=0.015):
    count=0
    while 1:
        count +=1
        if count % 2 == 0:
            print "pausing"
            pause()
        else:
            print "resuming"
            resume()
        time.sleep(interval)

def add_vt(line):
    global pIDS
    print 'adding to virtual time'
    pIDS += 'line '

# use with tm 10 and loop topo

################################################


def run_main():
    global hosts
    global net
    global controlNetwork 
    top = topo()
    if args.onos:
        controlNetwork = onos.ONOSCluster('c0', args.numControllers)
        net = Mininet(top,
                      controller=[ controlNetwork],
                      switch=onos.ONOSOVSSwitch)#, failMode = 'standalone' )
    else:
        net = Mininet(top, link = TCLink)
    
    # if we call ovs dilate first maybe the threads will be in vt
    if args.ovs_vt:
        ovs_dilate()
    net.start()
    if args.ovs_vt:
        ovs_dilate()
    if args.onos:
        pass
    #fix
    #net.dilateEmulation(1,0) # param 1 is tdf param 2 is if we should dilate controller 
    #net.dilateEmulation(1,0)
    
    # set IPs in hosts
    for i in hosts:
        net.get(i.get_host_name()).setIP(i.get_ip())
    
    print('Dumping Host Connections')
    dumpNodeConnections(net.hosts)

    #net.waitConnected()

    pidList(net)
 
    global startTime
    startTime = time.time()
    print('initiation finished')  

    CLI(net)

''' 
The IED configuration file dictates what command each host should run on startup

tm (test mode) 4 or greater will not call start processes -- this is for debugging purposes. 
find more in the debug document

'''


def start_processes(net):
    # start commands

    if args.test_mode < 4:
        for i in hosts:
            print i.get_process_command()
            net.get(i.get_host_name()).cmd(i.get_process_command())
        
    setup_pipes(net)

    if os.fork():
        pipe_listen(net)


if args.onos:
    OldCLI=onos.CLI
else:
    OldCLI=CLI

'''
This class extends the Mininet CLI

'''

class DSSnetCLI( OldCLI ):
    "CLI extensions for DSSnet"

    prompt = 'DSSnet -->  ' 
    
    def __init__( self,net, **kwargs ):
        OldCLI.__init__( self,net, **kwargs )

    def DSSnet( self, line):
        pass

    def do_pause( self, line):
        pause()

    def do_resume( self, line):
        resume()

    def do_start( self, line ):
        start_processes(net)

    def do_setup_pipes(self, line):
        setup_pipes(net)
    
    def do_show_freeze(self, line):
        net.showFreezeStatus()

    def do_show_dilation(self, line):
        net.showDilation()
    
    def do_exit(self, line):
        ovs_restore()
        result = subprocess.Popen('./clean.sh')
        exit()
    
    def do_pause_unpause(self, line):
        l=line.split(' ')
        print l
        if args.test_mode < 4:
            pause_unpause(1,1,l[0],l[1])
        else: 
            pause_unpause(1,2,l[0],l[1])
    
    def do_custom_ping(self, line):
        custom_ping(float(line))

    def do_add_vt(self, line):
        add_vt(line)

###########################

CLI = DSSnetCLI

if __name__ == '__main__':
    # in case we died in a bad state
    ovs_restore()
    resume_ovs()

    setLogLevel = args.logLevel
    if args.c:
        ovs_restore()
        result = subprocess.Popen('./clean.sh')
        exit()
    run_main()

# fin



