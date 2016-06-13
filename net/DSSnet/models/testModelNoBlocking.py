import pipe
import time
import sys

pipout=pipe.setup_pipe_l(sys.argv[1])
pipin = pipe.setup_pipe_w()

time.sleep(10)

while 1:
    pipe.send_sync_event('update n p pre_pmu post_pmu %s a1 0\n' % time.time(), pipin)
    time.sleep(30)

# listen and print
