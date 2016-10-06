#####################
# power coordinator #
#####################
#  channon@iit.edu  #
#####################
#      DSSnet       #
#    Version 2.2    #
#####################

import win32com.client
import zmq
import numpy
from numpy import array
import sys
import argparse
from gen import updateG
from load import updateL
import load
import ied
import DSSnet_handler as handler
import time
import math

###########
#  Setup  #
###########

parser = argparse.ArgumentParser(description= 'Manages power system simulation and synchronizes with the network coordinator')
parser.add_argument('--version', action='version',version='DSSnet 2.2')
parser.add_argument('-ip', help='ip of power coordinator',default='216.47.152.23',type=str)
parser.add_argument('-port', help='port reserved for power coordinator',default='50021',type=str)
parser.add_argument('-IED','--IED_config', help='path to IED file',default='C:\DSS\DSSnet\dss/4bus\IED.config',type=str)
parser.add_argument('-cf','--circuit_filename', help='path to main circuit file',default = 'C:\DSS\DSSnet\dss/4bus\master.dss', type=str)
parser.add_argument('-ts','--timestep', help='resolution of time step',default=0.001,type=float)
parser.add_argument('-et', help='time the experiment should end',default=10.0,type=float)
parser.add_argument('-mode', help='mode the simulator should be ran in: "snapshot", "duty", ', default = 'duty',type=str)
args = parser.parse_args()

engine=win32com.client.Dispatch("OpenDSSEngine.DSS")
engine.Start("0")
engine.Text.Command='clear'
circuit=engine.ActiveCircuit

previous_time=0.0#in seconds used to compute intervals in between calls

def setupCircuit():
    print('starting circuit')
    engine.Text.Command='compile '+ args.circuit_filename
    #engine.Text.Command='solve'
    #engine.Text.Command='set mode=dynamics number=1'
    engine.Text.Command='solve mode=duty number=1'
    #engine.Text.Command='solve'
    print('circuit compiled')
 
# socket to network coordinator
def setupSocket():
    print('setting up socket')
    contextIn = zmq.Context()
    serverIn = contextIn.socket(zmq.REP)
    serverIn.bind("tcp://*:%s" % (args.port))
    print('socket is setup')
    return serverIn

##################
#  load in IEDs  #
##################

pmu = []
loads = []
gens = []
monitors = []

def read_config():
    with open(args.IED_config, 'r') as ied_config:
        for line in ied_config:
            if line[0] != '#':
                ied = line.split()
                if ied[0] =='load':
                    add_load(ied)
                if ied[0] =='gen':
                    add_gen(ied)
                if ied[0] =='pmu':
                    add_pmu(ied)
                if ied[0] =='monitor':
                    add_monitor(ied)


#load = load
def add_load(ied):
    loads.append(ied[1])

#gen = generator
def add_gen(ied):
    gens.append(ied[1])

# pmu = monitor
def add_pmu(ied):
    pmu.append(ied[1])

def add_monitor(ied):
    monitors.append(ied[1])

######################
#  Helper Functions  #
######################

def print_vsource():
    source = engine.ActiveCircuit.vsource
    return source

def getBusVolts():
    busNames=engine.ActiveCircuit.AllBusNames
    n_bus=len(busNames)

    V1_tup= engine.ActiveCircuit.AllBusVolts
    V1=array(V1_tup)
    V1=V.reshape(n_bus,3,2)
    return V1

def updateLoads(t):
    for x in loads:
        result = updateL(x,t)
        #print('%s: %s'%(x,result))
        update_controllable_loads(x,result)

def updateGeneration(t):
    for x in gens:
        result = updateG(x,t,args.timestep)       
        #print('%s: %s'%(x,result))
        update_controllable_gens(x,result)

def update_controllable_loads(load,val):
    #print('load.%s.kW=%s'% (str(load),str(val)))
    engine.Text.Command= 'load.%s.kW=%s'% (str(load),str(val))

def update_controllable_gens(gen,val):
    engine.Text.Command= 'generator.%s.kW=%s'% (str(gen),str(val))
    
def read_monitor(element): # mode 0
    DSSMonitors = circuit.Monitors
    direct('sample')

    DSSMonitors.saveAll()
    DSSMonitors.Name = element
    time=DSSMonitors.dblHour[0]
    v1 = DSSMonitors.Channel(1)[0]
    vang1 = DSSMonitors.Channel(2)[0]
    v2 = DSSMonitors.Channel(3)[0]
    vang2 = DSSMonitors.Channel(4)[0]
    v3 = DSSMonitors.Channel(5)[0]
    vang3 = DSSMonitors.Channel(6)[0]
    i1 = DSSMonitors.Channel(7)[0]
    iang1 = DSSMonitors.Channel(8)[0]
    i2 = DSSMonitors.Channel(9)[0]
    iang2 = DSSMonitors.Channel(10)[0]
    i3 = DSSMonitors.Channel(11)[0]
    iang3 = DSSMonitors.Channel(12)[0]
    freq = DSSMonitors.dblFreq[0]

    #clear
    DSSMonitors.resetAll()
    return ('%d %d %d %d %d %d %d %d %d %d %d %d %d %d' % 
            ( freq, 
                v1, vang1,
                v2, vang2,
                v3, vang3,
                i1, iang1,
                i2, iang2,
                i3, iang3,
                time))

def get_power_sensor(name): ## mode 1
    DSSMonitors = circuit.Monitors
    #3print(DSSMonitors.name)
    #DSSMonitors.name = name
    #DSSMonitors.reset()
    #print(DSSMonitors.name)
    #engine.Text.Command='solve'
    #print('hi')
    direct('sample')

    DSSMonitors.saveAll()

      
    
    s1 = DSSMonitors.Channel(1)[len(DSSMonitors.Channel(1))-1]
    s2 = DSSMonitors.Channel(3)[len(DSSMonitors.Channel(3))-1]
    s3 = DSSMonitors.Channel(5)[len(DSSMonitors.Channel(5))-1]
    a1 = DSSMonitors.Channel(2)[len(DSSMonitors.Channel(2))-1]
    a2 = DSSMonitors.Channel(4)[len(DSSMonitors.Channel(4))-1]
    a3 = DSSMonitors.Channel(6)[len(DSSMonitors.Channel(6))-1]

    p1 = s1*math.cos(math.radians(a1))
    p2 = s2*math.cos(math.radians(a2))
    p3 = s3*math.cos(math.radians(a3))
    #print('S: %s %s %s ' %(s1,s2,s3))
    #print('A: %s %s %s ' %(a1,a2,a3))
    print('P: %s %s %s ' %(p1,p2,p3))
    #engine.Text.Command='export monitor mon_wind_gen'
    return ('%s %s %s' %(p1,p2,p3))

def fault(name,phase,node1,node2):
    if node2 == 'a' :
        print('New Fault.%s phases=%s Bus1=%s' % (name,phase,node1))
        engine.Text.Command='New Fault.%s phases=%s Bus1=%s' % (name,phase,node1)
    else:
        engine.Text.Command='New Fault.%s phases=%s Bus1=%s Bus2=%s' % (name,phase,node1,node2)
        print('New Fault.%s phases=%s Bus1=%s Bus2=%s' % (name,phase,node1,node2))

def energyStorage(name, p1,p2,p3):
    #print('generator.%s.kW=%s'%(g_name,gen))
    
    engine.Text.Command = 'Storage.%s1.kW = %s'% (name, str(abs(float(p1))))

    engine.Text.Command = 'Storage.%s2.kW = %s'% (name ,str(abs(float(p2))))

    engine.Text.Command = 'Storage.%s3.kW = %s'% (name , str(abs(float(p3))))


    return 'ok' 

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func,k,kwargs[k])
        return func
    return decorate

def get_gen(gen_id,t):
    return str(updateG(gen_id,t,args.timestep))

def direct(cmd):
    engine.Text.Command=cmd
    
def updateTime(dt):
    cmd='set sec=%s' % str(float(dt)-1.0)
    engine.Text.Command=cmd
    updateLoads(dt)
    updateGeneration(dt)
    engine.Text.Command='solve'

def exportMonitors():
    #print('hi')
    for m in monitors:
        direct('export monitor %s' % m)
        print('export getmonitor %s' % m)

@static_vars(previous_time=float(-0.5))
def get_up_to_date(t): # solve for time step up until previous time
    #print('iterpolating')
    if get_up_to_date.previous_time < 0.0:
        get_up_to_date.previous_time = t
        #print('You should only see this once! %s'%type(get_up_to_date.previous_time))
        return 0

    time=t#-0.0005 # force round down I dont think we need cuz of round function
    iterations = int((round(time,3)-round(get_up_to_date.previous_time,3))/args.timestep) 
    #print('iterations: %s'%iterations)
    for i in range(iterations):
        dt =get_up_to_date.previous_time + args.timestep
        updateTime(dt)
        direct('sample')
        get_up_to_date.previous_time = dt    
    
    print(get_up_to_date.previous_time)
    if get_up_to_date.previous_time > args.et:

        exportMonitors()
        exit()

##############################
#  communicate with Comm net #
##############################

def commNet(serverIn):
    #print('waiting for request')
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')
    line0 = requestIn_str
    #print('%s\n'%line0)
    line=line0.split()
    if line[0] == 'update':
        print ('update request recieved from emulation coordinator: %s' % line0)
        length=len(line)

        # what does mininet want us to do????
        if length > 1 :
            newTime = line[5]
            get_up_to_date(float(newTime))
            updateTime(newTime)

            reply='ok'
            
            #do preprocessing
            try:
                #time.sleep(4)
                preprocess=getattr(handler,line[3])
                pre_processed_event=preprocess(line)
                # RUN MAIN EVENT
                funkName = pre_processed_event
                try:
                    #print(funcName)
                    processed_event = eval(funkName)
                except NameError:
                    print('error with eval %s' % pre_processed_event)
                    exit()

            except AttributeError:
                print('error with pre_processed_event %s' % line)

            #do postprocessing
            try:
                postprocess=getattr(handler,line[4])
                reply=postprocess(line,processed_event)
                #print(reply)
            except AttributeError:
                print('error with post %s' % line)
            
            ok=reply.encode('utf-8')
            print(ok)
            serverIn.send(ok)

            return (1)
        else:
            print('request recieved but with no content')
            # solve anyway? crash? ignore?  
    elif line[0] == 'test':
        print('\ntest message recieved\n')
        tmp = 'copy that netCoord, read you loud and clear, over\n'
        ok=tmp.encode('utf-8')
        serverIn.send(ok)

    ok='ok'.encode('utf-8')
    serverIn.send(ok)

def main():
    setupCircuit()
    server = setupSocket()
    read_config()
    while True:
        commNet(server)

main()