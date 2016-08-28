#!/usr/bin/python

# this program recieves the message from program A and prints it to a file

import signal,os
import time
import sys
import gtod

RUN_TIME = 60 # seconds
if len(sys.argv) > 1:
    print('hi')
    RUN_TIME = int(sys.argv[1])


def setup_pipe():
    pipe_name = '/tmp/vtime_test.pipe'
    if not os.path.exists(pipe_name):
        os.mkfifo(pipe_name)
    return open(pipe_name, 'r')
    
def listen(pipe):
    return pipe.readline()

if __name__ == '__main__':
    start_time = gtod.time()
    my_pipe = setup_pipe()
    while gtod.time() < (start_time + RUN_TIME):
        A = listen(my_pipe)
        if A:
            print('Program A GToD: %sProgram B GToD: %s \n' % ( A , time.time()))
