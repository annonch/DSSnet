# channon@iit.edu
import zmq
import time
import threading
import os
import sys
 
myIP = sys.argv[1]
ListenPort = sys.argv[2]
es_IP = sys.argv[3]
es_port = sys.argv[4]

#initialize values
gen_val = 0
load_1_val = 0
load_2_val = 0
load_3_val = 0
load_4_val = 0

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

# listen to Loads/Generator
contextIn = zmq.Context()
serverIn = contextIn.socket(zmq.REP)
ServerIn.bind("tcp://%s:%s" % (myIP,ListenPort))

# sent to Energy Storage Device
contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (es_IP,es_port))

# scheduler function
def do_every(interval, worker_func, iterations = 0):
    if iterations !=1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
        ).start();
    worker_func();

def func(l1,l2,l3,l4,g):
    dif = g - (l1+l2+l3+l4) 
    if dif > 0:
        charge(dif)
    if dif < 0:
        discharge(dif)

def charge(dif):
    send_es('charge %s' % dif)

def discharge(dif):
    send_es('discharge %s' % abs(dif))

def send_es(msg):
    msg_bytes=msg.encode('utf-8')
    clientOut.send(msg_bytes)
    result=clientOut.recv()

def listen():
    requestIn_bytes = serverIn.recv()
    requestIn=requestIn_bytes.decode('utf-8')
    ok='ok'.encode('utf-8')
    serverIn.send(ok)
    if (requestIn):
        line = requestIn.split()
        if line[0] == 'load1':
            load_1_val = int(line[1])
        elif line[0] == 'load2':
            load_2_val = int(line[1])
        elif line[0] == 'load3':
            load_3_val = int(line[1])
        elif line[0] == 'load4':
            load_4_val = int(line[1])
        elif line[0] == 'gen':
            gen_val = int(line[1])


do_every(1,func(load_1_val,load_2_val,load_3_val,load_4_val,gen_val))

while 1:
    listen()
