#!/usr/bin/python

import signal,os
import sys

pipe_read = ''
def setup_pipe_w():
    
    # pipe to coord
    pipe_name = './tmp/coordination.pipe'
    if not os.path.exists(pipe_name):
        os.mkfifo(pipe_name)
    pipeout = os.open(pipe_name, os.O_WRONLY)
    return pipeout

def setup_pipe_l(name):
    global pipe_read,pipein

    pipe_read = './tmp/%s' % name
    if not os.path.exists(pipe_read):
        os.mkfifo(pipe_read)

    return open(pipe_read, 'r')

        
def send_sync_event(update,pipeout):
    os.write(pipeout, (update))

def listen(pipein):
    return pipein.readline()
