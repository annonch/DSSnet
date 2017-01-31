
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

pipout = pipe.setup_pipe_l(es_ID)
#pipin = pipe.setup_pipe_w()

logging.basicConfig(filename='%s.log'%es_ID,level=logging.DEBUG)

#setup ports
contextIn =zmq.Context()
serverIn = contextIn.socket(zmq.REP)
print("tcp://%s:%s" % (myIP,myPort))
serverIn.bind("tcp://*:%s" % (myPort))

time.sleep(4)

while 1:
    requestIn_bytes = serverIn.recv()
    requestIn_str = requestIn_bytes.decode('utf-8')
    print('recieved %s: '%requestIn_str)
    ok = 'ok'.encode('utf-8')
    serverIn.send(ok)

