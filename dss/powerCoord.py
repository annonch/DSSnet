 #####################
# power coordinator #
#####################
#  channon@iit.edu  #
#####################
#      DSSnet       #
#    Version 2.2    #
#####################

#import win32com.client
import zmq
import numpy
from numpy import array
import sys
import argparse
import DSSnet_handler as handler
import dss_util
import time
import os.path
import math
## nw
import opendssdirect as DSS

###########
#  Setup  #
###########

parser = argparse.ArgumentParser(description= 
    'Manages power system simulation and synchronizes with the network coordinator')
parser.add_argument('-trace', 
                        help='"-trace 1" for yes: instead of using network emulator we can use a trace of synchronization events from file', 
                        default=0,type=int)
parser.add_argument('-trace_file', help = 'location for trace file',
                        default ='/home/dssnet/Projects/dssnet/dss/test/synch.config', type=str  )
parser.add_argument('--version', action='version',
                        version='DSSnet 3.0')
parser.add_argument('-ip', help='ip of power coordinator',
                        default='localhost',type=str)
parser.add_argument('-port', help='port reserved for power coordinator',
                        default='50021',type=str)
parser.add_argument('-IED','--IED_config', help='path to IED file',
                        default='/home/dssnet/Projects/dssnet/dss/test/IED.config',type=str)
parser.add_argument('-cf','--circuit_filename', help='path to main circuit file',
                        default = '/home/dssnet/Projects/dssnet/dss/test/master.dss', type=str)
parser.add_argument('-ts','--timestep', help='resolution of time step',
                        default=0.001,type=float)
parser.add_argument('-et', help='time the experiment should end',
                        default=2.0,type=float)
parser.add_argument('-mode', help='mode the simulator should be ran in: "Snap", "Duty", "Harmonics", "Direct","Dynamics": default is duty ', 
                        default = 'duty',type=str)
parser.add_argument('-mode_number','-mn', 
                        help='number of solutions done in different modes. Warning this advances the clock (I believe that you can just set the timestep to a good value and be okay)',
                        default='1',type=str)
args = parser.parse_args()

## Lets make sure the user has input values that we expect and are all valid ##

# mode stuff 
args.mode = args.mode.lower()
modes = 'harmonics' , 'snap', 'duty', 'dynamics', 'direct'
if args.mode in modes:
    print('%s mode detected' % args.mode)
else:
    print('ERROR: Invalid mode detected please choose one of: "Snap", "Duty", "Harmonics", "Direct","Dynamics"')
    print('EXITING')
    exit(-2)
try:
    int(args.mode_number)
except ValueError:
    print('ERROR: mode_number must be a string representation of an integer')
    print('EXITING')
    exit(-3)
    
### START up connection to OpenDSS ###
DSS._utils.dss_py.use_com_compat(True)
engine = DSS._utils.dss_py.DSS
#engine=win32com.client.Dispatch("OpenDSSEngine.DSS")
#if not engine.Start("0"):
#    print('ERROR: Can not start engine')
#    print('EXITING')
#    exit(-1)

trace=[]
if args.trace:
    print('%s%s'% ('\n Experiment running in trace mode from synch.config', 
            '\n --------------------------------------'))
    trace = dss_util.readfile(args.trace_file)


engine.Text.Command='clear'
circuit=engine.ActiveCircuit

previous_time=0.0#in seconds used to compute intervals in between calls

def setupCircuit():
    print('starting circuit')

    engine.Text.Command='compile '+ args.circuit_filename
    if args.mode == 'harmonics' or args.mode == 'dynamics':
        engine.Text.Command='solve mode=direct'
    engine.Text.Command='solve mode=%s number=%s' % (args.mode, args.mode_number)
    print('circuit compiled')
 
# socket to network coordinator
def setupSocket():
    print('setting up socket')
    contextIn = zmq.Context()
    serverIn = contextIn.socket(zmq.REP)
    serverIn.bind("tcp://*:%s" % (args.port)) # IP address is bound on whatever our IP address is
    print('socket is setup')
    return serverIn

## decorator for setting static function variables ##
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func,k,kwargs[k])
        return func
    return decorate




##################
#  load in IEDs  #
##################

pmu = []
loads = []
gens = []
monitors = []
# more ieds?

def read_config():
    with open(args.IED_config, 'r') as ied_config:
        for line in ied_config:
            if line[0] != '#':
                ied = line.split()
                if ied[0] =='load':
                    add_load(ied)
                if ied[0] =='gen':
                    add_gen(ied)
                if ied[0] =='monitor':
                    add_monitor(ied)


#load = load
def add_load(ied):
    loads.append(ied[1])

#gen = generator
def add_gen(ied):
    gens.append(ied[1])

def add_monitor(ied):
    monitors.append(ied[1])


##############################
#  communicate with Comm net #
##############################

def commNet(serverIn):
    
    ok = 'ok'
    line0 = readNext(serverIn)

    line=line0.split()
    if line[0] == 'update':
        print ('update request recieved from emulation coordinator: %s' % line0)
        length=len(line)

        # what does netCoord want us to do????
        if length > 1 :
            newTime = line[5]
            go = dss_util.get_up_to_date(engine,float(newTime),args,loads,gens)
            
            # time exceeded
            if go == 'end':
            	# exit cleanly and tell netcoord to exit
                print('experiment finished: %s' % ok)
                send(go,serverIn)
                f = finish()
                exit(f)
            # process event

            dss_util.updateTime(engine,newTime,loads,gens,args.et)

            reply='ok'
            
            #do preprocessing
            

            try:
                preprocess=getattr(handler,line[3])
                reply=preprocess(circuit,engine,args,line)
                # RUN MAIN EVENT
               

            except AttributeError:
                print('ERROR: with pre_processed_event %s' % line)
                print('EXITING')
                exit(-5)
            
            print('sending reply: %s' % reply)
            send(reply,serverIn)
            return (1)

        else:
            print('request recieved but with no content')
            # solve anyway? crash? ignore?  
    elif line[0] == 'test':
        print('\ntest message recieved\n')
        tmp = 'copy that netCoord, read you loud and clear, over\n'
        ok = tmp

    elif line[0] == 'exit':
        send('exit',serverIn)
        exit(-4)

    send(ok,serverIn)

def readNext(serverIn):
    # normal
    if not args.trace:
        requestIn_bytes = serverIn.recv()
        requestIn_str = requestIn_bytes.decode('utf-8')
        return requestIn_str
    

    # trace based
    else:
        return nextTrace()

@static_vars(current_trace=0)
def nextTrace():
    try: 
       t = trace[nextTrace.current_trace]
       nextTrace.current_trace+=1
    except IndexError:
        print ('trace finished... adding bogus update to end experiment')
        t = 'update b p a b %s a 0' % str(float(args.et)+1.0)
    return t

def send(s,server):
    if not args.trace:
        ok=str(s).encode('utf-8')
        server.send(ok)
    else:
        print('result: %s' % s)


def finish():
    dss_util.exportMonitors(engine,monitors)
    # if we need to do anything upon finish
    # do it here
    return 0


def main():
    setupCircuit()
    server = setupSocket()
    read_config()
    while True:
        commNet(server)

main()  
