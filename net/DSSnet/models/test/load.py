'''
test dssNet load
'''

import pipe
import sys
import time
import logging

Load_ID = sys.argv[1]

logging.basicConfig(filename='%s.log'%Load_ID,level=logging.DEBUG)

pipeout=pipe.setup_pipe_l(Load_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_netCoord(val):
    update = 'update n p controllable_load post_controllable_load %s %s 1 %s\n' %(time.time(),Load_ID, val)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

while 1:
    time.sleep(1.5)
    send_netCoord(10700)
