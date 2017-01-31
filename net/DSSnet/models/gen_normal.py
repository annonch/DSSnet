
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




logging.basicConfig(filename='%s.log'%Gen_ID,level=logging.DEBUG)

contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (server_IP,server_Port))
print('talking on %s:%s'%(server_IP,server_Port))
# open pipe to communicate to opendss

pipeout=pipe.setup_pipe_l(Gen_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_cc(val):

    
    global gen_val1
    global gen_val2
    global gen_val3

    gens = val.split()
    
    gen_val1 = float(gens[0])
    gen_val2 = float(gens[1])
    gen_val3 = float(gens[2])

    dif1 = gen_val1 + 1292.0
    dif2 = gen_val2 + 1039.0#(573 + load_1_val + load_2_val/2)                                                   
    dif3 = gen_val3 + 1252.0#(880 + load_3_val + load_2_val/2)                                                   

    print('difs')
    print(dif1)
    print(dif2)
    print(dif3)

    send_es('%s %s %s %s '% (dif1, dif2, dif3, time.time()))



def send_es(vall):
    val = vall.encode('utf-8')
    clientOut.send(val)
    print 'sent but waiting for response'
    status=clientOut.recv()
    logging.debug('sent message to cc: %s '%val)
    print 'sent'

def get_val():
    update = 'update b p pre_gen_report post_gen_report %s %s 1 mon_wind_gen\n' %(time.time(),Gen_ID)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

def t():
    print(time.time())

time.sleep(2)# for sync to start properly


if os.fork():

    while 1:
        #listen to response and send to cc
        x = pipe.listen(pipeout)
        if x:
            print x
            send_cc(x)
        time.sleep(0.001)
while 1:
    time.sleep(TIME_INT)
    get_val()
