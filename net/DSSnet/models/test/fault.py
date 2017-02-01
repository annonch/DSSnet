'''
test dssNet fault
'''

import pipe
import sys
import time
import logging

Fault_ID = sys.argv[1]

logging.basicConfig(filename='%s.log'%Fault_ID,level=logging.DEBUG)

pipeout=pipe.setup_pipe_l(Fault_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_netCoord():
    update = 'update n p fault post_fault %s %s 3 1 b24 a\n' %(time.time(),Fault_ID)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

time.sleep(1)
send_netCoord()

while 1:
    time.sleep(1)
