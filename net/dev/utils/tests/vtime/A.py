#!/usr/bin/python

#this program will test if v time is working or not


#
import signal,os
import sys
import time
import gtod

def setup_pipe():
    pipe_name = '/tmp/vtime_test.pipe'
    if not os.path.exists(pipe_name):
        os.mkfifo(pipe_name)
    pipeout = os.open(pipe_name, os.O_WRONLY)
    return pipeout

def send(msg,pipe):
    msg_n = '%s\n'%msg
    try:    
        os.write(pipe, msg_n.encode('utf-8'))
    except BrokenPipeError:
        # exit quietly..
        exit()

if __name__ == '__main__':
    my_pipe = setup_pipe()
    while 1:
        send(str(gtod.time()),my_pipe)
        time.sleep(2)
