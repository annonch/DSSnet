
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

Load_ID = sys.argv[1]
server_IP = sys.argv[2]
server_Port = sys.argv[3]

contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (server_IP,server_Port))

# open pipe to communicate to opendss

pipeout=pipe.setup_pipe_l(Load_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_cc(val):
    req_bytes = val.encode('utf-8')
    clientOut.send(req_bytes)
    status=clientOut.recv()

def get_val():
    update = 'update b p pre_load_report post_load_report %s %s 0\n' %(time.time(),Load_ID)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

# scheduler function
def do_every(interval, worker_func, iterations = 0):
    if iterations !=1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
        ).start();
    worker_func();

do_every(1,get_val)
