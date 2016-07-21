

# listen for message from control center 
  # if message update OpenDSS value

import zmq
import time
import sys
import os
import pipe

es_ID = sys.argv[1]
myIP = sys.argv[2]
myPort = sys.argv[3]

pipout = pipe.setup_pipe_l(es_ID)
pipin = pipe.setup_pipe_w()

#setup ports
contextIn =zmq.Context()
serverIn = contextIn.socket(zmq.REP)
serverIn.bind("tcp://%s:%s" % (myIP,myPort))

def openDSS(info):
    line=info.split()
    if line[0] == 'charge':
        val1= line[1]
        val2=0.001
    elif line[0] == 'discharge':
        val1=0.001
        val2=line[1]

    update = 'update n p pre_energyStorage post_energyStorage %s %s 2 %s %s' % (time.time(),es_ID,val1,val2)
    pipe.send_sync_event(update.encode('UTF-8'),pipin)
    
while 1:
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')
    if requestIn_str:
        openDss(requestIn_str)
