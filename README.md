# DSSnet #

### Requirements for installation: ###
* Ubuntu / Debian ( Debian >> Ubuntu ) probably will work on windows and osx.. (not tested yet)
* Vagrant
* Virtual-box 
* Windows VM 

###  Use  ###
* DSSnet combines a power grid simulator (OpenDSS) with a SDN emulator (mininet). The software is designed to get high fidelity results of smart grid networks that require both communication and power. 
* Version 2.0

## How do I get set up? ##

#### Set up the network emulation ####
* get this repository
* navigate to LINUX-FAST/
* run vagrant up
* run vagrant ssh to log in
* see vagrant docs for more info on vagrant (other useful commands vagrant destroy and vagrant halt)

#### I want to build everything the long way (everything will be very updated) ####
* navigate to LINUX-SLOW/
* run vagrant up (this takes about 2-3 hours or less depending on Internet and processor)
* vagrant ssh
* sudo reboot (IMPORTANT - we have recompiled the kernel with the latest virtual time kernel)
* wait 60 seconds
* vagrant ssh - now everything is setup
* go to virtual/VirtualTimeKernel/test_virtual_time/
* run `sudo make`
* run `sudo make install`
* run `sudo make install`
* go to virtual/VirtualTimeKernel/mininet 
* run `sudo make`
* run `sudo make install`
* run `sudo make install`

#### Setup Windows ####
* Get windows VM (win 7 onwards)
* Get python + numpy, win32com, (andaconda is easy for this stuff) [ tutorial to come, vagrant? ] 
* text editor

#### Setup Network  ####
* open port on windows, default 50021
* make sure to test that the linux vm can communicate with the windows vm (try telnet)

#### test ####
* on windows navigate to win folder in repository
* run `python powerCoord.py -ip x.x.x.x` whatever the ip of your win vm is (you can use bridged adapter under virtualbox settings to get a ip to the outside world)
* navigate to  DSSnet/net/DSSnet/ on linux
* run `sudo python netCoord.py -ip x.x.x.x whatever the ip of your win vm is
* You should see 
```
Opening Connection to tcp://10.47.142.26:50021
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 
*** Adding switches:
s1 s2 
*** Adding links:
(s1, h1) (s1, s2) (s2, h2) 
*** Configuring hosts
h1 h2 
*** Starting controller
c0 
*** Starting 2 switches
s1 s2 ...
Dumping Host Connections
h1 h1-eth0:s1-eth2
h2 h2-eth0:s2-eth2
pids in virtual time:   24230 24232 24237 24240 24223
python ./models/testModelNoBlocking.py h1 &

python ./models/testModelBlocking.py h2 &
creating pipe: ./tmp/h1 
creating pipe: ./tmp/h2 
initiation finished
*** Starting CLI:
mininet> 
```
* basically you should then see in 10 seconds 
```
update n p pre_pmu post_pmu 1465928573.14 a1 0
update b p pre_pmu post_pmu 1465928573.14 a1 0
update n p pre_pmu post_pmu 1465928573.14 a1 0
407202 7199 0 7199 -120 7199 119 334 -35 331 -154 341 85
update b p pre_pmu post_pmu 1465928573.14 a1 0
407202 7199 0 7199 -120 7199 119 334 -35 331 -154 341 85
``` 
* what this is doing is setting up a IEEE 4 bus system and with a monitor on line one at bus 1 acting as a pmu
* This tests the blocking and non-blocking queues and verifies connectivity to the simulation. 
* __always start the power coordinator first__
* the numbers returned are time and the pmu raw measurements


### Moving Forward ###
* now that the code is working you can start by creating the DSS circuit.
* create an entry for each IED in the IED configuration file in windows
* create a load/generation entry or pre/post configuration entry in the corresponding python files in windows
* create an IED model for your IEDs that run in the emulation in linux
* create a topology and ied configuration file in linux
*  create a controller application (more to come)

### Who do I talk to? ###
To seek help, and feature requests:

* Christopher Hannon
* Channon@hawk.iit.edu
* open an issue - I'll try to help!

# Docs #

## Linux  ##

### Sync Event ###

* Synchronization events come in two varieties:
* Blocking - Will pause all hosts in network to maintain temporal accuracy
* Not blocking - Will not pause hosts in network
* see paper in PADS for more details 

#### Sync Event Format ####

* space delimited
* `update b/nb destination(n/p) preprocessing_handler post_handler time hostID NumFields(n) f(1) f(2) ... f(n) `
* ex.:  `update nb p pow_default post_d 10.02341 Load101 1 50` Change value of load 101 to 50 kW
* ex.:  `update b p pow_default post_d 10.05683 PDC1001 5 PMU101 PMU102 PMU103 PMU1004 PMU1005` Request values of PMUs


### IED Models ###

* By default all models should have a pipe from the coordinator to their process to receive messages
* For IEDs this is how they get values from the power simulator
* For other hosts it may not be necessary 
* the class to import is `pipe.py`
* the name of the pipe is `./tmp/hostid.pipe`

#### Existing Models ####

none 

## Files ##

### IPC ###

* `pipe.py`
*  a model will call `pipe.setup_pipe(hostname)` passing in its own hostname
*  a model will call `pipe.send_sync_event(update)` to pass a synchronization event to the network coordinator
*  if a reply is expected from the synchronization event ( depending on the type of events (( see paper )) ) a call to `pipe.listen()` returns a string data if there is any data in the pipe. Typically a use would be `while i: if listen(): i=0` Im sure there are other/ better ways.


### store process metadata ###
* `DSSnet_hosts.py`
* This program contains host objects after reading in the configuration file

### sync event handler ###
* user defined synchronization preprocessing 
* post processing
* ** This file determines how models will interface with power coordinator **
todo - add more description

## Configs ##

### IED config ###

* contains the information for starting the models in the network emulator
* field 1 is unique identifier for the id of the host
* field 2 is a description of the host 
* field 3 is the assigned ip address
* field 4 is the startup command for the host - can use && |& ; etc
* keyword split is used to deliminate the field


#### format ####
* id split msg split ip split command
* `PMU101 split PMU split 1.2.3.4 split python pmu.py 101 pdc5 1.4.2.5 pmu101 > log.txt

### topo config ###
* defines switches links and linkops

#### format ####
* new switch_id
* a b linkops




## FAQ ##


no questions yet



## Troubleshooting ##

I get an error: Exception Please shut down the controller which is running on port 6653?

```
sudo python netCoord.py 
Opening Connection to tcp://10.47.142.26:50021
*** Creating network
*** Adding controller
Traceback (most recent call last):
  File "netCoord.py", line 291, in <module>
    run_main()
  File "netCoord.py", line 256, in run_main
    net = Mininet(top, link = TCLink)
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 172, in __init__
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 444, in build
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 411, in buildFromTopo
  File "build/bdist.linux-x86_64/egg/mininet/net.py", line 261, in addController
  File "build/bdist.linux-x86_64/egg/mininet/node.py", line 1539, in DefaultController
  File "build/bdist.linux-x86_64/egg/mininet/node.py", line 1362, in __init__
  File "build/bdist.linux-x86_64/egg/mininet/node.py", line 1380, in checkListening
Exception: Please shut down the controller which is running on port 6653:
Active Internet connections (servers and established)
tcp        0      0 127.0.0.1:52615         127.0.0.1:6653          TIME_WAIT   -               
tcp        0      0 127.0.0.1:52618         127.0.0.1:6653          TIME_WAIT   -               
tcp6       0      0 :::6653                 :::*                    LISTEN      22734/java      
```

well you should reserve this port for the controller. 

