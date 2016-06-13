#!usr/bin/python

#####################
#  channon@iit.edu  #
#####################

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, OVSKernelSwitch, RemoteController, Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel, info

####################
#  System Imports  #
####################

import sys
import time
import os
import subprocess


######################
#  helper functions  #
######################

# bash commands
PIDQ = "sudo pgrep -f mininet: > tmp/pidlist"
#old
#PAUSE  ="sudo pgrep -f mininet: | sudo awk  \'{system(\"sudo kill --signal SIGSTOP -\"$1)}' -"
#RESUME ="sudo pgrep -f mininet: | sudo awk  \'{system(\"sudo kill --signal SIGCONT -\"$1)}' -"
#new

pIDS=''

def pidList():
    global pIDS
    list = subprocess.call(PIDQ,shell=True)
    with open('tmp/pidlist', 'r') as ins:
        for line in ins:
            pIDS+= ('%s%s' %(' -',line.rstrip('\n')))  
    print (pIDS)

pidList()

NPAUSE = 'sudo kill --signal SIGSTOP%s'%pIDS
NRESUME ='sudo kill --signal SIGCONT%s'%pIDS

def pause():
    process = subprocess.call(NPAUSE, shell=True)
    time.sleep(0.2)
    process = subprocess.call(NRESUME, shell=True)
    time.sleep(0.01)

class DssTopo(Topo):
    "DSS custom topo"
    
    def build(self):
        
        ################
        #  start TOPO  #
        ################
        host1= self.addHost('host1')

        host2= self.addHost('host2')

        s1=self.addSwitch('switch1')
        s2=self.addSwitch('switch2')
        s3=self.addSwitch('switch3')
        s4=self.addSwitch('switch4')
        s5=self.addSwitch('switch5')
        s6=self.addSwitch('switch6')
        s7=self.addSwitch('switch7')
        s8=self.addSwitch('switch8')
        s9=self.addSwitch('switch9')
        s10=self.addSwitch('switch10')
        s11=self.addSwitch('switch11')
        s12=self.addSwitch('switch12')
        s13=self.addSwitch('switch13')
        s14=self.addSwitch('switch14')
        s15=self.addSwitch('switch15')
        s16=self.addSwitch('switch16')
        s17=self.addSwitch('switch17')
        s18=self.addSwitch('switch18')
        s19=self.addSwitch('switch19')
        s20=self.addSwitch('switch20')
        s21=self.addSwitch('switch21')
        s22=self.addSwitch('switch22')
        s23=self.addSwitch('switch23')
        s24=self.addSwitch('switch24')
        s25=self.addSwitch('switch25')
        s26=self.addSwitch('switch26')
        s27=self.addSwitch('switch27')
        s28=self.addSwitch('switch28')
        s29=self.addSwitch('switch29')
        s30=self.addSwitch('switch30')
        s31=self.addSwitch('switch31')
        s32=self.addSwitch('switch32')
        s33=self.addSwitch('switch33')
        s34=self.addSwitch('switch34')
        s35=self.addSwitch('switch35')
        s36=self.addSwitch('switch36')
        s37=self.addSwitch('switch37')
        s38=self.addSwitch('switch38')
        s39=self.addSwitch('switch39')
        s40=self.addSwitch('switch40')
        s41=self.addSwitch('switch41')
        s42=self.addSwitch('switch42')
        s43=self.addSwitch('switch43')
        s44=self.addSwitch('switch44')
        s45=self.addSwitch('switch45')
        s46=self.addSwitch('switch46')
        s47=self.addSwitch('switch47')
        s48=self.addSwitch('switch48')
        s49=self.addSwitch('switch49')
        s50=self.addSwitch('switch50')
        s51=self.addSwitch('switch51')
        s52=self.addSwitch('switch52')
        s53=self.addSwitch('switch53')
        s54=self.addSwitch('switch54')
        s55=self.addSwitch('switch55')
        s56=self.addSwitch('switch56')
        s57=self.addSwitch('switch57')
        s58=self.addSwitch('switch58')
        s59=self.addSwitch('switch59')
        s60=self.addSwitch('switch60')
        s61=self.addSwitch('switch61')
        s62=self.addSwitch('switch62')
        s63=self.addSwitch('switch63')
        s64=self.addSwitch('switch64')
        s65=self.addSwitch('switch65')
        s66=self.addSwitch('switch66')
        s67=self.addSwitch('switch67')
        s68=self.addSwitch('switch68')
        s69=self.addSwitch('switch69')
        s70=self.addSwitch('switch70')
        s71=self.addSwitch('switch71')
        s72=self.addSwitch('switch72')
        s73=self.addSwitch('switch73')
        s74=self.addSwitch('switch74')
        s75=self.addSwitch('switch75')
        s76=self.addSwitch('switch76')
        s77=self.addSwitch('switch77')
        s78=self.addSwitch('switch78')
        s79=self.addSwitch('switch79')
        s80=self.addSwitch('switch80')
        s81=self.addSwitch('switch81')
        s82=self.addSwitch('switch82')
        s83=self.addSwitch('switch83')
        s84=self.addSwitch('switch84')
        s85=self.addSwitch('switch85')
        s86=self.addSwitch('switch86')
        s87=self.addSwitch('switch87')
        s88=self.addSwitch('switch88')
        s89=self.addSwitch('switch89')
        s90=self.addSwitch('switch90')
        s91=self.addSwitch('switch91')
        s92=self.addSwitch('switch92')
        s93=self.addSwitch('switch93')
        s94=self.addSwitch('switch94')
        s95=self.addSwitch('switch95')
        s96=self.addSwitch('switch96')
        s97=self.addSwitch('switch97')
        s98=self.addSwitch('switch98')
        s99=self.addSwitch('switch99')
        s100=self.addSwitch('switch100')





        self.addLink(host1, s1, 
                     bw=10, delay='2ms')
        self.addLink(s1,s2,bw=10, delay='2ms')
        self.addLink(s2,s3,bw=10, delay='20ms')
        self.addLink(s3,s4,bw=10, delay='20ms')
        self.addLink(s4,s5,bw=10, delay='20ms')
        self.addLink(s5,s6,bw=10, delay='20ms')
        self.addLink(s6,s7,bw=10, delay='20ms')
        self.addLink(s7,s8,bw=10, delay='20ms')
        self.addLink(s8,s9,bw=10, delay='20ms')
        self.addLink(s9,s10,bw=10, delay='20ms')
        self.addLink(s10,s11,bw=10, delay='20ms')
        self.addLink(s11,s12,bw=10, delay='20ms')
        self.addLink(s12,s13,bw=10, delay='20ms')
        self.addLink(s13,s14,bw=10, delay='20ms')
        self.addLink(s14,s15,bw=10, delay='20ms')
        self.addLink(s15,s16,bw=10, delay='20ms')
        self.addLink(s16,s17,bw=10, delay='20ms')
        self.addLink(s17,s18,bw=10, delay='20ms')
        self.addLink(s18,s19,bw=10, delay='20ms')
        self.addLink(s19,s20,bw=10, delay='20ms')
        self.addLink(s20,s21,bw=10, delay='20ms')
        self.addLink(s21,s22,bw=10, delay='20ms')
        self.addLink(s22,s23,bw=10, delay='20ms')
        self.addLink(s23,s24,bw=10, delay='20ms')
        self.addLink(s24,s25,bw=10, delay='20ms')
        self.addLink(s25,s26,bw=10, delay='20ms')
        self.addLink(s26,s27,bw=10, delay='20ms')
        self.addLink(s27,s28,bw=10, delay='20ms')
        self.addLink(s28,s29,bw=10, delay='20ms')
        self.addLink(s29,s30,bw=10, delay='20ms')
        self.addLink(s30,s31,bw=10, delay='20ms')
        self.addLink(s31,s32,bw=10, delay='20ms')
        self.addLink(s32,s33,bw=10, delay='20ms')
        self.addLink(s33,s34,bw=10, delay='20ms')
        self.addLink(s34,s35,bw=10, delay='20ms')
        self.addLink(s35,s36,bw=10, delay='20ms')
        self.addLink(s36,s37,bw=10, delay='20ms')
        self.addLink(s37,s38,bw=10, delay='20ms')
        self.addLink(s38,s39,bw=10, delay='20ms')
        self.addLink(s39,s40,bw=10, delay='20ms')
        self.addLink(s40,s41,bw=10, delay='20ms')
        self.addLink(s41,s42,bw=10, delay='20ms')
        self.addLink(s42,s43,bw=10, delay='20ms')
        self.addLink(s43,s44,bw=10, delay='20ms')
        self.addLink(s44,s45,bw=10, delay='20ms')
        self.addLink(s45,s46,bw=10, delay='20ms')
        self.addLink(s46,s47,bw=10, delay='20ms')
        self.addLink(s47,s48,bw=10, delay='20ms')
        self.addLink(s48,s49,bw=10, delay='20ms')
        self.addLink(s49,s50,bw=10, delay='20ms')
        self.addLink(s50,s51,bw=10, delay='20ms')
        self.addLink(s51,s52,bw=10, delay='20ms')
        self.addLink(s52,s53,bw=10, delay='20ms')
        self.addLink(s53,s54,bw=10, delay='20ms')
        self.addLink(s54,s55,bw=10, delay='20ms')
        self.addLink(s55,s56,bw=10, delay='20ms')
        self.addLink(s56,s57,bw=10, delay='20ms')
        self.addLink(s57,s58,bw=10, delay='20ms')
        self.addLink(s58,s59,bw=10, delay='20ms')
        self.addLink(s59,s60,bw=10, delay='20ms')
        self.addLink(s60,s61,bw=10, delay='20ms')
        self.addLink(s61,s62,bw=10, delay='20ms')
        self.addLink(s62,s63,bw=10, delay='20ms')
        self.addLink(s63,s64,bw=10, delay='20ms')
        self.addLink(s64,s65,bw=10, delay='20ms')
        self.addLink(s65,s66,bw=10, delay='20ms')
        self.addLink(s66,s67,bw=10, delay='20ms')
        self.addLink(s67,s68,bw=10, delay='20ms')
        self.addLink(s68,s69,bw=10, delay='20ms')
        self.addLink(s69,s70,bw=10, delay='20ms')
        self.addLink(s70,s71,bw=10, delay='20ms')
        self.addLink(s71,s72,bw=10, delay='20ms')
        self.addLink(s72,s73,bw=10, delay='20ms')
        self.addLink(s73,s74,bw=10, delay='20ms')
        self.addLink(s74,s75,bw=10, delay='20ms')
        self.addLink(s75,s76,bw=10, delay='20ms')
        self.addLink(s76,s77,bw=10, delay='20ms')
        self.addLink(s77,s78,bw=10, delay='20ms')
        self.addLink(s78,s79,bw=10, delay='20ms')
        self.addLink(s79,s80,bw=10, delay='20ms')
        self.addLink(s80,s81,bw=10, delay='20ms')
        self.addLink(s81,s82,bw=10, delay='20ms')
        self.addLink(s82,s83,bw=10, delay='20ms')
        self.addLink(s83,s84,bw=10, delay='20ms')
        self.addLink(s84,s85,bw=10, delay='20ms')
        self.addLink(s85,s86,bw=10, delay='20ms')
        self.addLink(s86,s87,bw=10, delay='20ms')
        self.addLink(s87,s88,bw=10, delay='20ms')
        self.addLink(s88,s89,bw=10, delay='20ms')
        self.addLink(s89,s90,bw=10, delay='20ms')
        self.addLink(s90,s91,bw=10, delay='20ms')
        self.addLink(s91,s92,bw=10, delay='20ms')
        self.addLink(s92,s93,bw=10, delay='20ms')
        self.addLink(s93,s94,bw=10, delay='20ms')
        self.addLink(s94,s95,bw=10, delay='20ms')
        self.addLink(s95,s96,bw=10, delay='20ms')
        self.addLink(s96,s97,bw=10, delay='20ms')
        self.addLink(s97,s98,bw=10, delay='20ms')
        self.addLink(s98,s99,bw=10, delay='20ms')
        self.addLink(s99,s100,bw=10, delay='20ms')
        
        self.addLink(host2, s2, 
                     bw=10, delay='2ms')

def test():
    topo = DssTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    
    with open("pause.test","a") as myfile:
        for x in range(0,200):
            st1 = net.pingPairFull()
            #print 'pausing'
            time.sleep(0.01)
            pause()
            myfile.write( repr(st1[0][2][3]))
            myfile.write('\n')

    with open("noPause.test","a") as myffile:
        for x in range(0,200):
            st1 = net.pingPairFull()
            #print 'pausing'
            time.sleep(0.01)
            pause()
            myffile.write( repr(st1[0][2][3]))
            myffile.write('\n')

        
            


    net.stop()    

if __name__ == '__main__':
   setLogLevel('info')
   test()
