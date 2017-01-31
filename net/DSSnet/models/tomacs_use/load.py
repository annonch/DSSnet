#!/usr/bin/python
# every 100ms
  # fuction: 
    # get value from opendss
    # send value of load to control center
import pipe
import sys
import time
import threading
import zmq
import os
import logging

TIME_INT = 0.15

Load_ID = sys.argv[1]
server_IP = sys.argv[2]
server_Port = sys.argv[3]

contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (server_IP,server_Port))

# open pipe to communicate to opendss

logging.basicConfig(filename='%s.log'%Load_ID,level=logging.DEBUG)

pipeout = pipe.setup_pipe_l(Load_ID)
pipin   = pipe.setup_pipe_w()

# send to control center
 
def send_cc(val):
    logging.debug('sending %s to cc at time %s'%(val,time.time()))
    val = '%s %s'%(Load_ID,val)
    req_bytes = val.encode('utf-8')
    clientOut.send(req_bytes)
    status=clientOut.recv()
    logging.debug('reply at %s' %time.time())

def get_val():
    update = 'update b p get_load_value post_get_load_value %s %s 0\n' %(time.time(),Load_ID)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

while 1:
    time.sleep(TIME_INT)
    get_val()

    x = pipe.listen(pipeout)
    
    if x:
        logging.debug(x)
        send_cc(x)

