
# listen for message from control center 
  # if message update OpenDSS value

import zmq
import time
import sys
import os
import pipe
import gtod

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

print('good to go')

def openDSS(info):
    line=info.split()
    t = gtod.time()
    #t = line[2]
    logging.debug('descrepency: %s' % str(float(line[2])-t))
    if line[0] == 'charge':
        val1= line[1]
        val2=0.001
    elif line[0] == 'discharge':
        val1=0.001
        val2=line[1]

    ph1 = line[0]
    ph2 = line[1]
    ph3 = line[2]

    update = 'update nb p pre_energyStorage post_energyStorage %s %s 3 %s %s %s\n' % (gtod.time(),es_ID,ph1,ph2,ph3)
    logging.debug('sending to pipe')
    pipe.send_sync_event(update.encode('UTF-8'),pipin)
    
while 1:
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')
    print('recieved %s: '%requestIn_str)
    ok = 'ok'.encode('utf-8')
    serverIn.send(ok)

    if requestIn_str:
        print('recieved: %s' % requestIn_str)
        logging.debug('got a request %s at %s' % (requestIn_str,gtod.time()))
        openDSS(requestIn_str)
        
    #time.sleep(0.01)
