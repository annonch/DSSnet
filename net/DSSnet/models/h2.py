
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



TIME_INT = 0.1

Gen_ID = sys.argv[1]
server_IP = sys.argv[2]
server_Port = sys.argv[3]

contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (server_IP,server_Port))
# open pipe to communicate to opendss

pipeout=pipe.setup_pipe_l(Gen_ID)
#pipin = pipe.setup_pipe_w()

logging.basicConfig(filename='%s.log'%Gen_ID)




#print 'starting\n'

# send to control center
def send_es():
    val = 'ok'.encode('utf-8')
    start_time = time.time()
    clientOut.send(val)
    status=clientOut.recv()

    logging.debug('%s' % str(time.time() - start_time))
    print '%s' %(str(time.time() - start_time))


while 1:
    time.sleep(TIME_INT)
    send_es()
    
