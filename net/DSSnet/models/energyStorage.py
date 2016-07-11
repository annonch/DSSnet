

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

pipout = pipe.setup_pipe_l(sys.argv[1])
pipin = pipe.setup_pipe_w()



def openDSS(info):
    line=info.split()
    if line[0] == 'charge':
        val1= line[1]
        val2=0
    elif line[0] = 'discharge':
        val1=0
        val2=line[1]

    update = 'update n p pre_energyStorage post_energyStorage %s %s 2 %s %s' % (time.time(),es_ID,val1,val2)
    pipe.send_sync_event(update,pipin)
    
while 1:
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')
    if requestIn_str:
        openDss(requestIn_str)
