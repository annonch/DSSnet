# channon@iit.edu
import zmq
import time
import threading
import os
import thread
import sys
import pipe
import logging

cc_ID = sys.argv[1] 
myIP = sys.argv[2]
ListenPort = sys.argv[3]
es_IP = sys.argv[4]
es_port = sys.argv[5]

logging.basicConfig(filename='%s.log'%cc_ID,level=logging.DEBUG)

#start
logging.debug('new run')

#initialize values
gen_val = 750.0
load_1_val = 250.0
load_2_val = 250.0
load_3_val = 250.0
load_4_val = 250.0

'''
# listen for messages from the generator
  # if new generator message
  # update gen_val to new value

# listen for messages from loads, 1 - 4
  # if new load message x
  # update load_x_val to new value

# every 100 ms
# run function
   # difference = gen - total load
   # if difference is positive
      # send message to energy storage to charge the difference
   # else difference is negitive
      # send message to energy storage to discharge battery
'''

pipeout=pipe.setup_pipe_l(cc_ID)
pipin = pipe.setup_pipe_w()


# listen to Loads/Generator
contextIn = zmq.Context()
serverIn = contextIn.socket(zmq.REP)
print("tcp://%s:%s" % (myIP,ListenPort))
serverIn.bind("tcp://%s:%s" % (myIP,ListenPort))

# sent to Energy Storage Device
contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
print("tcp://%s:%s" % (es_IP,es_port))
clientOut.connect("tcp://%s:%s" % (es_IP,es_port))

# scheduler function
def do_every(interval, worker_func, iterations = 0):
    if iterations !=1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
        ).start();
    worker_func();

def func():
    global load_1_val
    global load_2_val
    global load_3_val
    global load_4_val
    global gen_val

    dif = gen_val - (load_1_val+load_2_val+load_3_val+load_4_val) 
    if dif > 0.0:
        charge(dif)
    if dif < 0.0:
        discharge(dif)

def charge(dif):
    send_es('charge %s \n' % str(dif))

def discharge(dif):
    send_es('discharge %s \n' % str(abs(dif)))

def send_es(msg):
    msg_bytes=msg.encode('utf-8')
    with com_lock:
        clientOut.send(msg_bytes)
        result=clientOut.recv()
    logging.debug('send: %s at time %s' % (msg,time.time()))

def listen():
    #logging.debug('in listen')
    requestIn_bytes = serverIn.recv()
    requestIn=requestIn_bytes.decode('utf-8')
    ok='ok'.encode('utf-8')
    serverIn.send(ok)

    logging.debug('recieved: %s'%requestIn)
    
    global load_1_val, load_2_val, load_3_val, load_4_val, gen_val
    
    if (requestIn):
        line = requestIn.split()
        if line[0] == 'load1':
            load_1_val = float(line[1])
        elif line[0] == 'load2':
            load_2_val = float(line[1])
        elif line[0] == 'load3':
            load_3_val = float(line[1])
        elif line[0] == 'load4':
            load_4_val = float(line[1])
        elif line[0] == 'gen':
            gen_val = float(line[1])

com_lock=thread.allocate_lock()

do_every(1,func)

while 1:
    listen()
    time.sleep(0.005)
    #func()
