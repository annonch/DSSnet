#!/usr/bin/python

#this program will test if v time is working or not


#
#import signal,os
#import sys
import time
#import gtod

def send(msg):
    print msg

if __name__ == '__main__':
    x=0     
    while x<700000000:
        if x % 15000000 ==0 :
            send(str(time.time()))
            #time.sleep(2)
        x+=1
