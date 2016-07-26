
# listen for message from control center 
  # if message update OpenDSS value

import zmq
import time
import sys
import os
import pipe

import logging

es_ID = sys.argv[1]
myIP = sys.argv[2]
myPort = sys.argv[3]

logging.basicConfig(filename='%s.log'%es_ID,level=logging.DEBUG)

pipout = pipe.setup_pipe_l(es_ID)
pipin = pipe.setup_pipe_w()

#setup ports
contextIn =zmq.Context()
serverIn = contextIn.socket(zmq.REP)
print("tcp://%s:%s" % (myIP,myPort))
serverIn.bind("tcp://%s:%s" % (myIP,myPort))

def openDSS(info):
    line=info.split()
    if line[0] == 'charge':
        val1= line[1]
        val2=0.001
    elif line[0] == 'discharge':
        val1=0.001
        val2=line[1]

    update = 'update b p pre_energyStorage post_energyStorage %s %s 2 %s %s\n' % (time.time(),es_ID,val1,val2)
    logging.debug('sending to pipe')
    pipe.send_sync_event(update.encode('UTF-8'),pipin)
    
while 1:
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')
    ok = 'ok'.encode('utf-8')
    serverIn.send(ok)

    if requestIn_str:
        openDSS(requestIn_str)
        logging.debug('got a request %s at %s'%(requestIn_str,time.time()))

    time.sleep(0.1)
