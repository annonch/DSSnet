'''
test dssNet energyStorage
'''

import pipe
import sys
import time
import logging

Es_ID = sys.argv[1]

logging.basicConfig(filename='%s.log'%Es_ID,level=logging.DEBUG)

pipeout=pipe.setup_pipe_l(Es_ID)
pipin = pipe.setup_pipe_w()

# send to control center
 
def send_netCoord(val1, val2, val3):
    update = 'update b p storage post_storage %s %s 3 %s %s %s\n' %(time.time(),Es_ID, val1, val2, val3)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

time.sleep(0.8)
send_netCoord(1950, 2050, -500)

while 1:
    time.sleep(1)
