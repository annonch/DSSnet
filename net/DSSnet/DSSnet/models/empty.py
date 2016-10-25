
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

TIME_INT = 10

Gen_ID = 'cc'#sys.argv[1]
server_IP = 'ld'#sys.argv[2]
server_Port = 'ld'#sys.argv[3]


'''
#initialize values                                                                                             
gen_val1 = 250.0
gen_val2 = 250.0
gen_val3 = 250.0
load_1_val = 250.0
load_2_val = 250.0
load_3_val = 250.0
load_4_val = 250.0
'''
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
'''
contextOut = zmq.Context()
clientOut = contextOut.socket(zmq.REQ)
clientOut.connect("tcp://%s:%s" % (server_IP,server_Port))
print('talking on %s:%s'%(server_IP,server_Port))
# open pipe to communicate to opendss
'''
pipeout=pipe.setup_pipe_l(Gen_ID)
pipin = pipe.setup_pipe_w()

# send to control center


while 1:
    time.sleep(TIME_INT)
    print'a'
