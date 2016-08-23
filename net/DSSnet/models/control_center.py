# channon@iit.edu
import zmq
import time
import threading
import os
import thread
import sys
import pipe
import logging
import gtod

cc_ID = sys.argv[1] 
myIP = sys.argv[2]
ListenPort = sys.argv[3]
es_IP = sys.argv[4]
es_port = sys.argv[5]

logging.basicConfig(filename='%s.log'%cc_ID,level=logging.DEBUG)

#start
logging.debug('new run')

#initialize values
gen_val1 = 250.0
gen_val2 = 250.0
gen_val3 = 250.0
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
    global gen_val1
    global gen_val2
    global gen_val3

    dif1 = gen_val1 - (1115 + load_4_val) 
    dif2 = gen_val2 - (573 + load_1_val + load_2_val/2)
    dif3 = gen_val3 - (880 + load_3_val + load_2_val/2)
    
    print('difs')
    print(dif1)
    print(dif2)
    print(dif3)
    
    send_es('%s %s %s %s '% (dif1, dif2, dif3, gtod.time()))

def send_es(msg):
    print('sending %s' % msg)
    msg_bytes=msg.encode('utf-8')
    with com_lock:
        clientOut.send(msg_bytes)
        result=clientOut.recv()
    logging.debug('send: %s at time %s' % (msg,gtod.time()))

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
        print('recieved message %s'%line)
        if line[0] == 'load1':
            load_1_val = float(line[1])
        elif line[0] == 'load2':
            load_2_val = float(line[1])
        elif line[0] == 'load3':
            load_3_val = float(line[1])
        elif line[0] == 'load4':
            load_4_val = float(line[1])
        elif line[0] == 'gen':
            gen_val1 = float(line[1])
            gen_val2 = float(line[2])
            gen_val3 = float(line[3])

com_lock=thread.allocate_lock()

do_every(0.1,func)

while 1:
    listen()
    time.sleep(0.005)
    #func()
