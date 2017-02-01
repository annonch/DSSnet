'''
test dssNet generation
'''

import pipe
import sys
import time
import logging

Gen_ID = sys.argv[1]

logging.basicConfig(filename='%s.log'%Gen_ID,level=logging.DEBUG)

pipeout=pipe.setup_pipe_l(Gen_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_netCoord(val):
    update = 'update n p controllable_generator post_controllable_generator %s %s 1 %s\n' %(time.time(),Gen_ID, val)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

while 1:
    time.sleep(1)
    send_netCoord(1.5)
