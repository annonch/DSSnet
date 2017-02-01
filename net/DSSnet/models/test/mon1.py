'''
test dssNet monitor
'''

import pipe
import sys
import time
import logging

Mon_ID = sys.argv[1]

logging.basicConfig(filename='%s.log'%Mon_ID,level=logging.DEBUG)

pipeout=pipe.setup_pipe_l(Mon_ID)
pipin = pipe.setup_pipe_w()
 
def send_netCoord():
    update = 'update b p monitor_1 post_monitor_1 %s %s 0 \n' %(time.time(),Mon_ID)
    pipe.send_sync_event(update.encode('UTF-8'), pipin)

def listen():
    message=pipe.listen(pipeout)
    logging.debug(message)



while 1:
    time.sleep(1.35)
    send_netCoord()
    listen()
