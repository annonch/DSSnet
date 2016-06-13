#!/bin/python

# file used for processing synchronization events

# pre-processing events

def pre_gen(msg,net,hosts):
    return msg

def pre_load(msg,net,hosts):
    return msg

def pre_pmu(msg,net,hosts):
    return msg


# post processing events

def post_load(event,reply,net,hosts):
    return reply

def post_gen(event,reply,net,hosts):
    return reply

def post_pmu(event,reply,net,hosts):
    print event
    print reply
    return reply
