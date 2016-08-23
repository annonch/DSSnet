
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
import gtod

TIME_INT = 0.1

Gen_ID = sys.argv[1]
server_IP = sys.argv[2]
server_Port = sys.argv[3]


logging.basicConfig(filename='%s.log'%Gen_ID,level=logging.DEBUG)

contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (server_IP,server_Port))

# open pipe to communicate to opendss

pipeout=pipe.setup_pipe_l(Gen_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_cc(val):
    val = ('%s %s' % (Gen_ID,val))
    req_bytes = val.encode('utf-8')
    clientOut.send(req_bytes)
    status=clientOut.recv()
    logging.debug('sent message to cc: %s '%val)

def get_val():
    update = 'update b p pre_gen_report post_gen_report %s %s 1 mon_wind_gen\n' %(gtod.time(),Gen_ID)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

def t():
    print(time.time())

# scheduler function
def do_every(interval, worker_func, iterations = 0):
    if iterations !=1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
        ).start();
    worker_func();

time.sleep(3)# for sync to start properly

do_every(TIME_INT,get_val)

#print time.time()

#do_every(TIME_INT,t,1)



while 1:
    #listen to response and send to cc
    x = pipe.listen(pipeout)
    if x:
        send_cc(x)
    time.sleep(0.001)
