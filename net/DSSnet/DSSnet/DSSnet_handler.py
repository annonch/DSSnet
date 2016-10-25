#!/bin/python
import models.pipe 

# file used for processing synchronization events

# pre-processing events

##################################

import pipes

def controllable_generator(msg,net,hosts):
    return msg

def controllable_load(msg,net,hosts):
    return msg

def storage(msg,net,hosts):
    return msg

def fault(msg,net,hosts):
    return msg

def monitor_0(msg,net,hosts):
    return msg

def monitor_1(msg,net,hosts):
    return msg

def get_load_value(msg,net,hosts):
    return msg

def get_gen_value(msg,net,hosts):
    return msg

###########


def post_get_load_value(event,reply,net,hosts,pipes):
    #print event
    i = (event.split()[6])
    value = reply
    models.pipe.send_sync_event('%s \n'%value,pipes[i])
    return reply

def post_get_gen_value(event,reply,net,hosts,pipes):
    #print event
    i = (event.split()[6])
    value = reply
    models.pipe.send_sync_event('%s \n'%value,pipes[i])
    return reply

def post_controllable_generator(event,reply,net,hosts,pipes):
    return reply

def post_controllable_load(event,reply,net,hosts,pipes):
    return reply

def post_energyStorage(event,reply,net,hosts,pipes):
    return reply

def post_fault(event,reply,net,hosts,pipes):
    return reply

def post_monitor_0(event,reply,net,hosts,pipes):
    i = (event.split()[6])
    value = reply
    models.pipe.send_sync_event('%s \n'%value,pipes[i])
    return reply

def post_monitor_1(event,reply,net,hosts,pipes):
    i = (event.split()[6])
    value = reply
    models.pipe.send_sync_event('%s \n'%value,pipes[i])
    return reply




#################################33
#              OLD
#################################33
'''
def pre_gen(msg,net,hosts):
    return msg

def pre_load(msg,net,hosts):
    return msg

def pre_pmu(msg,net,hosts):
    return msg



def pre_link_down(msg,net, hosts):
    a = msg[8]
    b = msg[9]
    print a
    print b
    print 'here we are'
    net.configLinkStatus(a,b,'down')
    return 0

def pre_link_down(msg,net, hosts):
    a = msg[8]
    b = msg[9]
    net.configLinkStatus(a,b,'down')
    return 0

# post processing events

def post_load(event,reply,net,hosts,pipes):
    return reply

def post_gen(event,reply,net,hosts,pipes):
    return reply

def post_pmu(event,reply,net,hosts,pipes):
    return reply

def post_link_down(event,reply,net,hosts,pipes):
    return reply

def post_link_up(event,reply,net,hosts,pipes):
    return reply

#### smt

def pre_load_report(msg,net,hosts):
    return msg

def pre_gen_report(msg,net,hosts):
    return msg

def post_load_report(event,reply,net,hosts,pipes):
    i = (event.split()[6])
    value = reply
    models.pipe.send_sync_event('%s \n'%value,pipes[i])
    return reply

def post_gen_report(event,reply,net,hosts,pipes):
    print event
    i = (event.split()[6])
    value = reply
    models.pipe.send_sync_event('%s \n'%value,pipes[i])
    return reply

def pre_energyStorage(msg,net,hosts):
    return msg

def post_energyStorage(event,reply,net,hosts,pipes):
    return reply




# end smt

def post_pmu(event, reply, net, hosts, pipes):
    even =  event.split()
    rep = reply.split()
    reorder = rep[1]+' '+rep[2]+' '+rep[3]+' '+rep[4]+' '+rep[5]+ ' '+rep[6]+' '+rep[7]+' '+rep[8]+' '+rep[9]+' '+rep[0]+ ' '+rep[0]
    
   
    models.pipe.send_sync_event(reorder, pipes['h1'])
    print 'we did it!'
    return reply
    
'''
