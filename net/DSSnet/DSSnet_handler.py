#!/bin/python
import models.pipe 

# file used for processing synchronization events

# pre-processing events

def pre_gen(msg,net,hosts):
    return msg

def pre_load(msg,net,hosts):
    return msg

def pre_pmu(msg,net,hosts):
    return msg


# post processing events

def post_load(event,reply,net,hosts, pipes):
    return reply

def post_gen(event,reply,net,hosts, pipes):
    return reply

def post_pmu2(event,reply,net,hosts, pipes):
    #print event
    print reply
    return reply

def post_pmu(event, reply, net, hosts, pipes):
    even =  event.split()
    rep = reply.split()
    reorder = rep[1]+' '+rep[2]+' '+rep[3]+' '+rep[4]+' '+rep[5]+ ' '+rep[6]+' '+rep[7]+' '+rep[8]+' '+rep[9]+' '+rep[0]+ ' '+rep[0]
    
   
    models.pipe.send_sync_event(reorder, pipes['h1'])
    print 'we did it!'
    return reply
    
