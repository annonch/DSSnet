#!/usr/bin/python

import sys
from ctypes import *

libgtod = cdll.LoadLibrary('./libgtod.so')

def time():
    #c_longdouble 
    gt = libgtod.gt
    gt.restype = c_longdouble
    t=gt()
    #print ('%0.6f'%t)
    #print str('%0.6f'%t)
    #print ('%0.6f' %float(str('%0.6f'%t)))
    return float(str('%0.6f'%t))

