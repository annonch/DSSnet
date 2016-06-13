# DSSnet #

### Requirements for installation: ###
* Ubuntu / Debian ( Debian >> Ubuntu )
* Vagrant
* Virtual-box 
* Windows VM (more on windows later)

###  Use  ###

* DSSnet combines a power grid simulator (OpenDSS) with a SDN emulator (mininet). The software is designed to get high fidelity results of smart grid networks that require both communication and power. 
* Version 2.0

## How do I get set up? ##

#### Set up the network emulation ####
* get this repository
* navigate to VMS/LINUX/Mininet/
* run vagrant up (this takes about 1 hour or less depending on Internet and processor)
* vagrant ssh
* sudo reboot (IMPORTANT - we have recompiled the kernel with the latest virtual time kernel)
* wait 60 seconds
* vagrant ssh - now everything is setup

#### Setup Windows ####
* Get windows VM
* Get python + numpy, win32com, (andaconda is easy for this stuff) [ tutorial to come ] 
* text editor

#### Setup Network  ####
* open port on windows, default 50021
* make sure to test that the vagrant vm can communicate with the windows vm

#### test ####

TODO: make test 

### Moving Forward ###

TODO:

### Who do I talk to? ###
To seek help, and to propose improvements (certainly welcome) talk to me.

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

* todo

## Files ##

### IPC ###

* `pipe.py`
*  a model will call `pipe.setup_pipe(hostname)` passing in its own hostname
* the model will call `pipe.send_sync_event(update)` to pass a synchronization event to the network coordinator
* if a reply is expected from the synchronization event ( depending on the type of events (( see paper )) ) a call to `pipe.listen()` returns a string data if there is any data in the pipe. Typically a use would be `while i: if listen(): i=0` Im sure there are other/ better ways.


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


## Windows ##
todo


## FAQ ##
no questions yet