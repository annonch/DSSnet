
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
serverIn.bind("tcp://*:%s" % (myPort))

load1 = 485.0
load2 = 170.0
load3 = 66.0
ph1 = 600.0
ph2 = 600.0
ph3 =600.0

def openDSS():
    
    global load1,load2,load3,ph1,ph2,ph3
    a = (807.0 + float(load1)) - (float(ph1))
    b = (973.0 + float(load3)) - (float(ph2))
    c = (1082.0 + float(load2))  - (float(ph3))
    logging.debug('%s : %s : %s : %s : %s :%s : %s : %s :%s ' % (a,b,c,ph1,ph2,ph3,load1,load2,load3))
    update = 'update b p storage post_storage %s %s 3 %s %s %s\n' % (time.time(),es_ID,a,b,c)
    logging.debug('sending to pipe %s'%update)
    pipe.send_sync_event(update.encode('UTF-8'),pipin)
    
def update(msg):
    global load1,load2,load3,ph1,ph2,ph3
    line = msg.split()
    idd = line[0]
    if idd == 'load1':
        load1 = line[1]
    if idd == 'load2':
        load2 = line[1]
    if idd == 'load3':
        load3 = line[1]
        
    if idd == 'gen':
        ph1 = line[1]
        ph2 = line[2]
        ph3 = line[3]    
        openDSS()


while 1:
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')

    print('recieved %s: '%requestIn_str)
    ok = 'ok'.encode('utf-8')
    serverIn.send(ok)

    if requestIn_str:
        print('recieved: %s' % requestIn_str)
        logging.debug('got a request %s at %s' % (requestIn_str,time.time()))
        update(requestIn_str)
        
    #time.sleep(0.01)
